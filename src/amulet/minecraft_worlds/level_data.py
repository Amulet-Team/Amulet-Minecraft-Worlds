from typing import TypeVar, Any

T = TypeVar("T")


def dynamic_cast(obj: Any, cls: type[T]) -> T:
    if isinstance(obj, cls):
        return obj
    raise TypeError(f"{obj} is not an instance of {cls}")


class LevelData:
    platform: str
    version: str
    origin: str
    level_name: str
    dim_height: dict[str, tuple[tuple[int, int, int], tuple[int, int, int]]]

    def __init__(self, data: dict) -> None:
        self._decode_data(data)

    def _decode_data(self, data: dict) -> None:
        world_data = dynamic_cast(data.pop("world_data"), dict)
        self._decode_metadata(world_data)
        if world_data:
            raise RuntimeError("Unhandled data in world_data")

        level_data = dynamic_cast(data.pop("level_data"), dict)
        self._decode_level_data(level_data)
        if level_data:
            raise RuntimeError("Unhandled data in level_data")

        dim_height = dynamic_cast(data.pop("dim_height"), dict)
        self._decode_dim_height(dim_height)

        if data:
            raise RuntimeError("Unhandled data in data")

    def _decode_metadata(self, world_data: dict) -> None:
        self.platform = dynamic_cast(world_data.pop("platform"), str)
        self.version = dynamic_cast(world_data.pop("version"), str)
        self.origin = dynamic_cast(world_data.pop("origin"), str)

    def _decode_level_data(self, level_data: dict) -> None:
        self.level_name = dynamic_cast(level_data.pop("level_name"), str)

    def _decode_dim_height(self, dim_height: dict) -> None:
        self.dim_height = {}
        for k, ((min_x, min_y, min_z), (max_x, max_y, max_z)) in dim_height.items():
            self.dim_height[dynamic_cast(k, str)] = (
                (
                    dynamic_cast(min_x, int),
                    dynamic_cast(min_y, int),
                    dynamic_cast(min_z, int),
                ),
                (
                    dynamic_cast(max_x, int),
                    dynamic_cast(max_y, int),
                    dynamic_cast(max_z, int),
                ),
            )


class WorldData(LevelData):
    modified_time: float
    max_version: tuple[int, ...]

    def _decode_level_data(self, level_data: dict) -> None:
        super()._decode_level_data(level_data)
        self.modified_time = dynamic_cast(level_data.pop("modified_time"), float)
        self.max_version = tuple(
            dynamic_cast(v, int)
            for v in dynamic_cast(level_data.pop("max_version"), list)
        )


class JavaLevelData(WorldData):
    pass


class BedrockLevelData(WorldData):
    pass
