#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "fastmcp>=3,<4",
#   "py-key-value-aio[filetree]",
# ]
# ///

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from typing import Callable, NoReturn, Protocol, cast
from urllib.parse import urlparse


DEFAULT_MCP_SERVER_NAME = "kepler"
DEFAULT_MCP_URL = "https://app.keplerbrowser.com/mcp"
DEFAULT_TOKEN_DIR = Path("~/.fastmcp/oauth-mcp-client-cache").expanduser()


class SupportsRun(Protocol):
    def run(
        self,
        *,
        transport: str | None = None,
        show_banner: bool | None = None,
        **transport_kwargs: object,
    ) -> None: ...


def fail(message: str) -> NoReturn:
    print(f"mcp-proxy-server.py: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_http_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        fail(f"expected an http(s) MCP URL, got: {url!r}")
    return url


def build_oauth(target_url: str) -> object:
    try:
        fastmcp_auth = importlib.import_module("fastmcp.client.auth")
        filetree_store_module = importlib.import_module("key_value.aio.stores.filetree")
    except ImportError:
        fail(
            "token persistence requires FastMCP auth storage dependencies. "
            "Launch with uv, for example: "
            "uv run .mcp-proxy-server.py"
        )

    OAuth = getattr(fastmcp_auth, "OAuth")
    FileTreeStore = getattr(filetree_store_module, "FileTreeStore")
    FileTreeV1CollectionSanitizationStrategy = getattr(
        filetree_store_module, "FileTreeV1CollectionSanitizationStrategy"
    )
    FileTreeV1KeySanitizationStrategy = getattr(
        filetree_store_module, "FileTreeV1KeySanitizationStrategy"
    )

    token_dir = Path(
        os.environ.get("KEPLER_OAUTH_TOKEN_DIR", str(DEFAULT_TOKEN_DIR))
    ).expanduser()
    token_dir.mkdir(parents=True, exist_ok=True)
    token_storage: object = FileTreeStore(
        data_directory=token_dir,
        key_sanitization_strategy=FileTreeV1KeySanitizationStrategy(token_dir),
        collection_sanitization_strategy=FileTreeV1CollectionSanitizationStrategy(
            token_dir
        ),
    )

    callback_port = os.environ.get("KEPLER_OAUTH_CALLBACK_PORT")
    oauth_kwargs: dict[str, object] = {
        "mcp_url": target_url,
        "token_storage": token_storage,
    }
    if callback_port:
        oauth_kwargs["callback_port"] = int(callback_port)

    return OAuth(**oauth_kwargs)


def create_mcp_proxy() -> SupportsRun:
    target_url = validate_http_url(os.environ.get("KEPLER_MCP_URL", DEFAULT_MCP_URL))
    server_name = os.environ.get("KEPLER_MCP_SERVER_NAME", DEFAULT_MCP_SERVER_NAME)

    try:
        fastmcp_server = importlib.import_module("fastmcp.server")
        fastmcp_transports = importlib.import_module("fastmcp.client.transports")
    except ImportError:
        fail(
            "fastmcp is not installed. Launch with uv, for example: "
            "uv run .mcp-proxy-server.py"
        )

    StreamableHttpTransport = getattr(fastmcp_transports, "StreamableHttpTransport")
    transport = StreamableHttpTransport(url=target_url, auth=build_oauth(target_url))

    create_proxy = cast(
        Callable[..., SupportsRun], getattr(fastmcp_server, "create_proxy")
    )
    return create_proxy(transport, name=server_name)


mcp = create_mcp_proxy()


if __name__ == "__main__":
    mcp.run(transport="stdio", show_banner=False)
