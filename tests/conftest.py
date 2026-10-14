"""
Shared pytest fixtures for CareerLens AI test suite.
"""

from __future__ import annotations

import socket
import sys
import threading
import time
from pathlib import Path

import pytest
import requests
import uvicorn

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import app


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def api_server_url():
    """Start uvicorn server in a background thread for live HTTP testing."""
    port = get_free_port()
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    base_url = f"http://127.0.0.1:{port}"

    # Wait for server to come up
    max_wait = 5.0
    start_time = time.time()
    ready = False
    while time.time() - start_time < max_wait:
        try:
            resp = requests.get(f"{base_url}/api/health", timeout=1.0)
            if resp.status_code == 200:
                ready = True
                break
        except Exception:
            time.sleep(0.1)

    if not ready:
        server.should_exit = True
        raise RuntimeError("FastAPI server failed to start within timeout.")

    yield base_url

    server.should_exit = True
