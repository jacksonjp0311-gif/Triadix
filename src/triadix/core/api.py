from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .node import TriadicNode
from ..models.block import Transaction


app = FastAPI(title="Triadix API", version="1.7.0")
NODE = TriadicNode("api-node")


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


@app.get("/")
def root():
    return {
        "project": "Triadix",
        "version": "1.7.0",
        "message": "Minimal network transport layer active."
    }


@app.get("/status")
def status():
    return NODE.status_snapshot()


@app.get("/chain")
def get_chain():
    return {
        "length": len(NODE.engine.chain),
        "chain": NODE.export_chain(),
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