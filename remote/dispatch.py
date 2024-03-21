"""Web requests to 3D printer RESTful interface."""

import aiohttp
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()
ENDPOINT = os.getenv("ENDPOINT")
PRINTER_PORT = 9000


class NodeForwarder:
    def __init__(self, port):
        self.port = port

    @property
    def url(self):
        return f"http://{ENDPOINT}:{self.port}"

    async def execute(self, command: str, payload: Optional[str] = "") -> str:
        url = f"{self.url}/{command}/{payload}"

        async with aiohttp.ClientSession() as session:
            await session.get(url)

    async def write(self, payload: str) -> str:
        await self.execute("writecf", payload)


class Printer(NodeForwarder):
    def __init__(self):
        super().__init__(port=PRINTER_PORT)

    async def move(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        payload = f"G1 X{x} Y{-y} Z{z}"
        await self.write(payload=payload)
