import os
import shutil
from typing import Iterable
import re
import json
from tempfile import mkdtemp


def _get_world_path(world_rpath: str) -> str:
    return os.path.join(__path__[0], "worlds_src", world_rpath)


def for_each_world(globals_, worlds: Iterable[str]):
    def wrap(cls: type):
        for world in worlds:
            world_identifier = re.sub(r"\W|^(?=\d)", "_", world)
            globals_[world_identifier] = type(
                world_identifier, (cls,), {"WorldPath": world}
            )
        return None

    return wrap


def _create_temp(path: str) -> tuple[str, str]:
    """Copy the file or directory at path to a temporary location and return this path.

    :param path: The path to copy.
    :return: The temporary directory path to clean up and the temporary path to the file/directory.
    """
    temp_dir = mkdtemp(prefix="amulet")
    temp_path = os.path.join(temp_dir, os.path.basename(path))
    shutil.copytree(path, temp_path)
    return temp_dir, temp_path


def _delete_path(path: str) -> None:
    """Clean a given path removing all data at that path."""
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
    elif os.path.isfile(path):
        os.remove(path)


class WorldTemp:
    _src_path: str
    _temp_dir: str | None
    path: str | None
    _metadata: dict | None

    def __init__(self, world_rpath: str):
        self._src_path = _get_world_path(world_rpath)
        self._temp_dir = None
        self.path = None
        self._metadata = None

    def __repr__(self) -> str:
        return f"WorldTemp({self._src_path})"

    @property
    def metadata(self) -> dict:
        if self._metadata is None:
            with open(os.path.join(self._src_path, "world_test_data.json")) as f:
                self._metadata = json.load(f)
        return self._metadata

    def __enter__(self):
        self._temp_dir, self.path = _create_temp(self._src_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _delete_path(self._temp_dir)
        self._temp_dir = None
        self.path = None


from .worlds_src import (
    BedrockLevels,
    JavaVanillaLevels,
    JavaForgeLevels,
    java_vanilla_1_12_2,
    java_vanilla_1_13,
    JavaLevels,
    Levels,
)
