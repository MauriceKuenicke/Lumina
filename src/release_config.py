from fastapi import FastAPI
import requests
import yaml
from schema import Schema, And, Use, Optional
import os
from .endpoints import API_PATH
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


def get_releases_file_path() -> str:
    """
    Return the relative path to the config file containing the product information.
    :return: str
    """
    in_docker = os.environ.get('IN_DOCKER')
    if in_docker:
        return '/app/releases.yaml'
    return 'releases.yaml'


def read_yaml_releases() -> release_location_schema:
    """
    Return the configuration for the release locations from the .yaml file.
    :return: dict
    """
    file_path = Path(get_releases_file_path())
    if not Path.exists(file_path):
        raise FileExistsError("No releases file found.")

    with open(file_path, "r") as stream:
        raw_releases = yaml.safe_load(stream)

    release_location_schema.validate(raw_releases)
    return raw_releases
