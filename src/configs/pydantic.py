from pydantic import ConfigDict

class ConfigPydantic:

    config_dict: ConfigDict = ConfigDict(
        arbitrary_types_allowed = True
    )