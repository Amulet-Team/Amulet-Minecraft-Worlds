from typing import TypeVar, Any

T = TypeVar('T')

def dynamic_cast(obj: Any, cls: type[T]) -> T:
    if isinstance(obj, cls):
        return obj
    raise TypeError(f"{obj} is not an instance of {cls}")


class LevelData:
    platform: str
    version: str
    origin: str
    dim_height: dict[str, tuple[tuple[int, int, int], tuple[int, int, int]]]

    def __init__(self, data: dict) -> None:
        self._decode_world_data(data)
        if data["world_data"]:
            raise RuntimeError("Unhandled data in world_data")
        del data["world_data"]

        self._decode_dim_height(data)

    def _decode_world_data(self, data: dict) -> None:
        self.platform = dynamic_cast(data["world_data"]["platform"], str)
        self.version = dynamic_cast(data["world_data"]["version"], str)
        self.origin = dynamic_cast(data["world_data"]["origin"], str)

    def _decode_dim_height(self, data: dict) -> None:
        self.dim_height = {}
        for k, ((min_x, min_y, min_z), (max_x, max_y, max_z)) in dynamic_cast(data["dim_height"], dict).items():
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
                )
            )


class JavaLevelData(LevelData):
    pass


class BedrockLevelData(LevelData):
    pass
