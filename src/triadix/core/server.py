import argparse
import uvicorn


def main():
    parser = argparse.ArgumentParser(description="Run a Triadix API node.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    uvicorn.run(
        "triadix.core.api:app",
        host=args.host,
        port=args.port,
        reload=False,
    )


if __name__ == "__main__":
    main()