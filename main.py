from __future__ import annotations

import sys

import uvicorn


def start_server() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except ValueError:
            pass

    print("Server started successfully")
    print("Running at:")
    print("http://localhost:8000")
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    start_server()
