from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class PeerRecord:
    peer_id: str
    base_url: str = ""
    label: str = ""
    added_at: float = 0.0

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class NodeIdentity:
    node_id: str
    label: str = ""
    base_url: str = ""
    created_at: float = 0.0

    def to_dict(self) -> Dict:
        return asdict(self)