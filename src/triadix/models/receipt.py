from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class TransactionReceipt:
    tx_id: str
    block_index: int
    included: bool
    sender: str
    receiver: str
    amount: float
    nonce: int
    hC: str

    def to_dict(self) -> Dict:
        return asdict(self)