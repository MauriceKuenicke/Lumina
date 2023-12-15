from fastapi import FastAPI, Query
import requests
import yaml
from schema import Schema, And, Use, Optional
import os
from .endpoints import API_PATH
from .release_config import read_yaml_releases
from pathlib import Path

app = FastAPI()

owner = "MauriceKuenicke"
repo = "pulsar-topic-viewer"


RELEASES = read_yaml_releases()
print(RELEASES)

for product in RELEASES:
    release_location = RELEASES[product]["location"]

    @app.get(f"/{product}/latest-release", tags=["Releases"],
             description=f"Return the latest release information from {release_location} "
                         f"in the format that Tauri expects.",
             summary=f"Latest Release information for {product}")
    async def return_latest_release_information(
            release_candidate: str = Query(product, include_in_schema=False)
    ):
        release_link = API_PATH["latest_release"].format(owner=str(owner), repo=str(repo))
        response = requests.get(release_link).json()
        return RELEASES[release_candidate]

