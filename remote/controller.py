"""Listen in on commands from bluetooth-connected console controller."""

from dataclasses import dataclass
from enum import Enum

import pygame


class Buttons(Enum):
    """Button index in the get_button call."""

    x = 0
    circle = 1
    square = 2
    triangle = 3
    up = 11
    down = 12
    left = 13
    right = 14


@dataclass
class State:
    x: float  # left joystick
    y: float  # left joystick
    buttons: dict[str, bool]

    def payload(self) -> dict[str, float | int]:
        """Parse payload to send to printer.

        Returns:
            dict[str, float|int]: x, y, and z movement (in mm).
        """

        z = 0.5 * (int(self.buttons["up"]) - int(self.buttons["down"]))
        return {"x": round(self.x), "y": round(self.y), "z": z}


class Controller:
    # We live life on the edge and assume that the
    # controller of interest is the first (only) one connected.
    joystick_index = 0

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()

        if joystick_count == 0:
            raise Exception("No joysticks detected")

        self.joystick = pygame.joystick.Joystick(Controller.joystick_index)
        self.joystick.init()

    def get(self) -> State:
        pygame.event.pump()  # Update internal state
        x = self.joystick.get_axis(0)
        y = self.joystick.get_axis(1)
        buttons: dict[str, bool] = dict()

        for button in Buttons:
            state = self.joystick.get_button(button.value)
            buttons[button.name] = state

        return State(x=x, y=y, buttons=buttons)
