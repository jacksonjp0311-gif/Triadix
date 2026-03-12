from triadix.core.http_client import (
    get_status,
    get_chain,
    submit_transaction,
    build_from_mempool,
    sync_chain,
)


def test_http_client_functions_exist():
    assert callable(get_status)
    assert callable(get_chain)
    assert callable(submit_transaction)
    assert callable(build_from_mempool)
    assert callable(sync_chain)