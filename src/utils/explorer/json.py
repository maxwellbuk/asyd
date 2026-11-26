from utils.explorer.file import PacketFiles

from configs.pydantic import ConfigPydantic

from pathlib import Path
import json

from json.decoder import JSONDecodeError

from pydantic import validate_call

class PacketJSON:

    @staticmethod
    @validate_call(config = ConfigPydantic.config_dict)
    async def create(
        object: list | dict,
        file: Path | str
    ) -> None:
        await PacketFiles.record_value(
            json.dumps(
                object,
                ensure_ascii = False,
                indent = 4
            ),
            file
        )

    @staticmethod
    @validate_call(config = ConfigPydantic.config_dict)
    async def read(
        file: Path | str
    ) -> list | dict:
        try:
            return json.loads(
                await PacketFiles.read_file(
                    file,
                    "str"
                )
            )
        except JSONDecodeError:
            raise ValueError(f"По пути: {file}, невалидный JSON")

    @staticmethod
    @validate_call(config = ConfigPydantic.config_dict)
    async def change_items_json(
        items: list | dict,
        file: Path | str
    ) -> None:
        current_json = await PacketJSON.read(file)

        types = {
            "current-json": type(current_json).__name__,
            "input-items": type(items).__name__
        }

        if not types["current-json"] in ["list", "dict"]:
            raise ValueError("JSON должен содержать список или словарь")

        if types["current-json"] != types["input-items"]:
            raise TypeError("JSON и входные данные отличаются по типу")

        match types["current-json"]:
            case "list":
                for index, element in enumerate(items):
                    if element == None: continue

                    if index > len(current_json) - 1:
                        raise IndexError(f"Индекс элемента в списке: {index}, выходит за список")

                    current_json[index] = element
            case "dict":
                for key, value in items.items():
                    if not key in current_json:
                        raise KeyError(f"Данный ключ: {key}, не находится в словаре")
                    current_json[key] = value

        await PacketJSON.create(
            current_json,
            file
        )