import yaml
from schema import Schema, And, Optional
import os
from pathlib import Path


supported_types = ["GitHub"]

release_location_schema = Schema(
    {
        Optional(str): {
            "location": And(str, lambda s: s in supported_types),
            "repo_owner": And(str, len),
            "repo_name": And(str, len),
            Optional("version_regex"): And(str, len),
        }
    }
)


class ReleaseTracker:
    def __init__(self, config: dict[str, dict[str, str]]):
        self._yaml_config = config

    @property
    def apps(self):
        return list(self._yaml_config.keys())

    def config_by_app(self, app: str) -> dict[str, str]:
        config = self._yaml_config.get(app, None)
        if not config:
            raise KeyError(f"Application settings not found for app: {app}")
        return config

    def app_release_location(self, app: str):
        config = self._yaml_config.get(app, None)
        if not config:
            raise KeyError(f"Application settings not found for app: {app}")

        return config.get("location", None)

    @classmethod
    def from_yaml(cls) -> "ReleaseTracker":
        """
        Return the configuration for the release locations from the .yaml file.
        :return: dict
        """
        file_path = cls.get_releases_file_path()
        if not Path.exists(file_path):
            raise FileExistsError("No releases file found.")

        with open(file_path, "r") as stream:
            raw_releases = yaml.safe_load(stream)

        release_location_schema.validate(raw_releases)
        return ReleaseTracker(raw_releases)

    @staticmethod
    def get_releases_file_path() -> Path:
        """
        Return the relative path to the config file containing the product information.
        :return: str
        """
        in_docker = os.environ.get('IN_DOCKER')
        if in_docker:
            return Path('/app/releases.yaml')
        return Path('releases.yaml')

