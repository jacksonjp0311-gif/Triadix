from triadix.core.orchestrator import (
    seed_demo_chain,
    persist_node_state,
    restore_node_state,
    http_flow_snapshot,
)


def main():
    node_a = "http://127.0.0.1:8001"
    node_b = "http://127.0.0.1:8002"
    state_file = "C:/Users/jacks/OneDrive/Desktop/Triadix/triadix-run/state/http_node_a_state.json"

    print("Triadix v2.2 persistence demo")
    print("")

    before = http_flow_snapshot(node_a, node_b)
    print("Before:")
    print(before)
    print("")

    seed_result = seed_demo_chain(node_a, blocks=12)
    print("Seed node A:")
    print(seed_result)
    print("")

    save_result = persist_node_state(node_a, state_file)
    print("Saved node A state:")
    print(save_result)
    print("")

    restore_result = restore_node_state(node_b, state_file)
    print("Loaded node A state into node B:")
    print(restore_result)
    print("")

    after = http_flow_snapshot(node_a, node_b)
    print("After:")
    print(after)


if __name__ == "__main__":
    main()