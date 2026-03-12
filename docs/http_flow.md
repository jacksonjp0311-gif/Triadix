# Triadix v1.9 HTTP Flow

This layer demonstrates a complete local HTTP path:

1. start node A on port 8001
2. start node B on port 8002
3. seed node A with a signed transaction over HTTP
4. build node A block from mempool over HTTP
5. fetch node A chain over HTTP
6. sync node B from node A over HTTP

This is still local transport, not full decentralized networking.