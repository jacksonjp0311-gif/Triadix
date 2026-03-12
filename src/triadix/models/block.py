from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float
    data: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Block:
    index: int
    previous_hE: str
    previous_hI: str
    previous_hC: str
    transactions: List[Transaction]
    timestamp: float
    hE: str
    hI: str
    hC: str
    E: float
    I: float
    dphi: float
    C: float

    def to_dict(self) -> Dict:
        return {
            "index": self.index,
            "previous": {
                "hE": self.previous_hE,
                "hI": self.previous_hI,
                "hC": self.previous_hC
            },
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "hE": self.hE,
            "hI": self.hI,
            "hC": self.hC,
            "metrics": {
                "E": self.E,
                "I": self.I,
                "dphi": self.dphi,
                "C": self.C
            }
        }