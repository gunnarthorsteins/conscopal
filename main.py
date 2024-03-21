"""Entry point for conscopal. Hit `python main.py`"""

import asyncio
from time import sleep

from remote import controller, dispatch

# The GET requests are async, but I'd still not
# go faster than 20 ms for not to overload the
# endpoint.
SLEEP_S = 0.02


async def main():
    joystick = controller.Controller()
    printer_ = dispatch.Printer()

    while True:
        state: controller.State = joystick.get()
        payload = state.payload()
        print(payload)
        await printer_.move(**payload)
        sleep(SLEEP_S)


if __name__ == "__main__":
    asyncio.run(main())
