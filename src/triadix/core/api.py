from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .node import TriadicNode
from .wallet import generate_wallet
from .transactions import sign_transaction
from ..models.block import Transaction


app = FastAPI(title="Triadix API", version="2.7.0")
NODE = TriadicNode(label="api-node")


class TransactionIn(BaseModel):
    sender: str
    receiver: str
    amount: float
    data: str = ""
    public_key: str = ""
    signature: str = ""
    nonce: int = 0
    tx_id: str = ""


class ChainSyncIn(BaseModel):
    chain: list[dict]
    checkpoints: dict[str, str] | None = None


class PeerIn(BaseModel):
    peer_id: str
    base_url: str = ""
    label: str = ""


class SeedDemoIn(BaseModel):
    blocks: int = 12


class SaveStateIn(BaseModel):
    filepath: str | None = None


class LoadStateIn(BaseModel):
    filepath: str


class IdentityIn(BaseModel):
    label: str | None = None
    base_url: str | None = None


class BuildIn(BaseModel):
    max_transactions: int | None = None


@app.get("/")
def root():
    return {
        "project": "Triadix",
        "version": "2.7.0",
        "message": "Triadix API node active."
    }


@app.get("/status")
def status():
    return NODE.status_snapshot()


@app.get("/receipts/{tx_id}")
def get_receipt(tx_id: str):
    receipt = NODE.engine.get_receipt(tx_id)
    if receipt is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt.to_dict()


@app.get("/chain")
def get_chain():
    return {
        "length": len(NODE.engine.chain),
        "chain": NODE.export_chain(),
        "checkpoints": NODE.engine.checkpoint_map(),
    }


@app.get("/peers")
def get_peers():
    return {
        "peer_count": len(NODE.peers),
        "peers": NODE.list_peers(),
    }


@app.post("/identity")
def set_identity(payload: IdentityIn):
    NODE.set_identity_metadata(label=payload.label, base_url=payload.base_url)
    return {
        "updated": True,
        "status": NODE.status_snapshot(),
    }


@app.post("/peers")
def add_peer(peer_in: PeerIn):
    NODE.add_peer(peer_in.peer_id, base_url=peer_in.base_url, label=peer_in.label)
    return {
        "registered": True,
        "peer_count": len(NODE.peers),
        "peers": NODE.list_peers(),
    }


@app.post("/transactions")
def submit_transaction(tx_in: TransactionIn):
    tx = Transaction(**tx_in.model_dump())
    try:
        if not NODE.engine.chain:
            NODE.engine.create_genesis_block()
        result = NODE.engine.submit_transaction(tx)
        return {
            "accepted": result["accepted"],
            "queued": result["queued"],
            "tx_id": result["tx_id"],
            "mempool_size": len(NODE.engine.mempool),
            "waiting_mempool_size": len(NODE.engine.waiting_mempool),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/build")
def build_from_mempool(payload: BuildIn | None = None):
    try:
        if not NODE.engine.chain:
            NODE.engine.create_genesis_block()
        max_transactions = payload.max_transactions if payload else None
        block = NODE.engine.build_block_from_mempool(max_transactions=max_transactions)
        return {
            "built": True,
            "block_index": block.index,
            "chain_length": len(NODE.engine.chain),
            "mempool_size": len(NODE.engine.mempool),
            "waiting_mempool_size": len(NODE.engine.waiting_mempool),
            "valid": NODE.engine.is_chain_valid(),
            "selection_report": NODE.engine.last_selection_report,
            "status": NODE.status_snapshot(),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))