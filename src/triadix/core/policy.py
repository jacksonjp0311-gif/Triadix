from dataclasses import dataclass


@dataclass
class SyncResult:
    adopted: bool
    reason: str
    local_length: int
    candidate_length: int
    checkpoint_verified: bool = True


class LongestValidChainPolicy:
    name = "longest_valid_chain"

    def choose(self, local_engine, candidate_engine, checkpoint_verified: bool = True) -> SyncResult:
        local_valid = local_engine.is_chain_valid()
        candidate_valid = candidate_engine.is_chain_valid()

        local_length = len(local_engine.chain)
        candidate_length = len(candidate_engine.chain)

        if not checkpoint_verified:
            return SyncResult(
                adopted=False,
                reason="candidate_checkpoint_mismatch",
                local_length=local_length,
                candidate_length=candidate_length,
                checkpoint_verified=False,
            )

        if not candidate_valid:
            return SyncResult(
                adopted=False,
                reason="candidate_invalid",
                local_length=local_length,
                candidate_length=candidate_length,
                checkpoint_verified=True,
            )

        if not local_valid:
            return SyncResult(
                adopted=True,
                reason="local_invalid_candidate_valid",
                local_length=local_length,
                candidate_length=candidate_length,
                checkpoint_verified=True,
            )

        if candidate_length > local_length:
            return SyncResult(
                adopted=True,
                reason="candidate_longer_valid",
                local_length=local_length,
                candidate_length=candidate_length,
                checkpoint_verified=True,
            )

        if candidate_length == local_length:
            return SyncResult(
                adopted=False,
                reason="same_length_keep_local",
                local_length=local_length,
                candidate_length=candidate_length,
                checkpoint_verified=True,
            )

        return SyncResult(
            adopted=False,
            reason="candidate_shorter",
            local_length=local_length,
            candidate_length=candidate_length,
            checkpoint_verified=True,
        )