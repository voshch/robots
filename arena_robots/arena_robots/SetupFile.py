from __future__ import annotations

import itertools
import typing
from collections.abc import Sequence

import attrs
import yaml
from arena_simulation_setup.tree import StaticProvider

from arena_robots import ARENA_ROBOTS_DIR


@attrs.define()
class Config:
    """Configuration for setting up a robot instance.
    """

    robot: str  # name of robot
    name: typing.Optional[str] = None  # name or name prefix
    planner: typing.Optional[str] = None  # nav2 planner
    controller: typing.Optional[str] = None  # nav2 controller
    behavior: typing.Optional[str] = None  # nav2 behavior tree

    extra: dict[str, typing.Any] = attrs.field(factory=dict)  # extra arbitrary data

    @classmethod
    def parse(cls, data: str | dict[str, typing.Any]) -> Sequence[Config]:
        """Parse a configuration from the given data.
        """
        if isinstance(data, str):
            return (cls(robot=data, name=data),)
        return tuple(cls(**data) for _ in range(data.pop('count', 1)))


class Provider(StaticProvider):

    def load(self) -> Sequence[Config]:
        with open(self.path, 'r') as f:
            configuration = yaml.safe_load(f)

        assert isinstance(configuration, list), "robot_setup.yaml must be a list"

        return list(itertools.chain.from_iterable(map(Config.parse, configuration)))


RobotSetup = Provider.bind(ARENA_ROBOTS_DIR / 'config' / 'setup')
