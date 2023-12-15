from fastapi import FastAPI, Query, HTTPException
import requests
from .endpoints import API_PATH
from .release_config import ReleaseTracker
from .utils import extract_version_string

app = FastAPI()

# Load release location configs into global memory
release_tracker: ReleaseTracker = ReleaseTracker.from_yaml()

for application in release_tracker.apps:
    release_location = release_tracker.app_release_location(app=application)

    @app.get(f"/{application}/latest-release", tags=["Releases"],
             description=f"Return the latest release information from {release_location} "
                         f"in the format that Tauri expects.",
             summary=f"Latest Release information for {application}")
    async def return_latest_release_information(
            release_candidate: str = Query(application, include_in_schema=False)
    ):
        config = release_tracker.config_by_app(app=release_candidate)
        owner, repo = config["repo_owner"], config["repo_name"]
        custom_regex = config.get("version_regex", None)

        release_data = get_latest_release_information_from_github(owner=owner, repo=repo)
        version = extract_version_string(release_data["tag_name"], custom_regex=custom_regex)
        if not version:
            raise HTTPException(
                status_code=404, detail=f"Couldn't extract the correct version number from: {release_data['tag_name']}."
                                        f" Please check your custom regex pattern if you have defined one."
            )
        notes = release_data["body"]
        pub_date = release_data["created_at"]
        return {
            "version": version,
            "notes": notes,
            "pub_date": pub_date
        }


def get_latest_release_information_from_github(owner: str, repo: str) -> dict[str, str]:
    release_link = API_PATH["latest_release"].format(owner=owner, repo=repo)
    github_api_response = requests.get(release_link)
    if github_api_response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=f"Couldn't find specified release information for owner: {owner} and repo: {repo}"
        )
    return github_api_response.json()


