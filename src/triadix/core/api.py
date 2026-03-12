from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .node import TriadicNode
from .wallet import generate_wallet
from .transactions import sign_transaction
from ..models.block import Transaction


app = FastAPI(title="Triadix API", version="2.3.0")
NODE = TriadicNode(label="api-node")


class TransactionIn(BaseModel):
    sender: str
    receiver: str
    amount: float
    data: str = ""
    public_key: str = ""
    signature: str = ""
    nonce: int = 0


class ChainSyncIn(BaseModel):
    chain: list[dict]


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


@app.get("/")
def root():
    return {
        "project": "Triadix",
        "version": "2.3.0",
        "message": "Triadix API node active."
    }


@app.get("/status")
def status():
    return NODE.status_snapshot()


@app.post("/identity")
def set_identity(payload: IdentityIn):
    NODE.set_identity_metadata(label=payload.label, base_url=payload.base_url)
    return {
        "updated": True,
        "status": NODE.status_snapshot(),
    }


@app.get("/chain")
def get_chain():
    return {
        "length": len(NODE.engine.chain),
        "chain": NODE.export_chain(),
    }


@app.get("/peers")
def get_peers():
    return {
        "peer_count": len(NODE.peers),
        "peers": NODE.list_peers(),
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
        NODE.engine.submit_transaction(tx)
        return {
            "accepted": True,
            "mempool_size": len(NODE.engine.mempool),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/build")
def build_from_mempool():
    try:
        if not NODE.engine.chain:
            NODE.engine.create_genesis_block()
        block = NODE.engine.build_block_from_mempool()
        return {
            "built": True,
            "block_index": block.index,
            "chain_length": len(NODE.engine.chain),
            "mempool_size": len(NODE.engine.mempool),
            "valid": NODE.engine.is_chain_valid(),
            "status": NODE.status_snapshot(),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/submit-and-build")
def submit_and_build(tx_in: TransactionIn):
    tx = Transaction(**tx_in.model_dump())
    try:
        if not NODE.engine.chain:
            NODE.engine.create_genesis_block()
        NODE.engine.submit_transaction(tx)
        block = NODE.engine.build_block_from_mempool()
        return {
            "accepted": True,
            "built": True,
            "block_index": block.index,
            "chain_length": len(NODE.engine.chain),
            "valid": NODE.engine.is_chain_valid(),
            "status": NODE.status_snapshot(),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/seed-demo")
def seed_demo(payload: SeedDemoIn):
    try:
        if not NODE.engine.chain:
            NODE.engine.create_genesis_block()

        private_key, public_key = generate_wallet()

        tx = Transaction(
            sender="demo-alice",
            receiver="demo-bob",
            amount=12.0,
            data="seed-demo-payment",
            public_key=public_key,
            nonce=NODE.engine.current_expected_nonce("demo-alice"),
        )
        sign_transaction(tx, private_key)

        NODE.engine.submit_transaction(tx)
        NODE.engine.build_block_from_mempool()

        while len(NODE.engine.chain) < payload.blocks:
            NODE.engine.add_block()

        return {
            "seeded": True,
            "chain_length": len(NODE.engine.chain),
            "status": NODE.status_snapshot(),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/sync")
def sync_chain(payload: ChainSyncIn):
    try:
        result = NODE.try_sync_from_chain_data(payload.chain)
        return {
            "adopted": result.adopted,
            "reason": result.reason,
            "local_length": result.local_length,
            "candidate_length": result.candidate_length,
            "status": NODE.status_snapshot(),
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/save-state")
def save_state(payload: SaveStateIn):
    try:
        path = NODE.engine.save_to_file(payload.filepath)
        return {
            "saved": True,
            "filepath": path,
            "status": NODE.status_snapshot(),
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/load-state")
def load_state(payload: LoadStateIn):
    try:
        NODE.engine = NODE.engine.load_from_file(payload.filepath)
        return {
            "loaded": True,
            "filepath": payload.filepath,
            "status": NODE.status_snapshot(),
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))