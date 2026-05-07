import os
import re
import zipfile
import requests


def parse_github_url(repo_url: str):
    """
    Iz GitHub URL-ja pridobi owner in repo.
    Primer:
    https://github.com/user/project -> user, project
    """
    pattern = r"github\.com/([^/]+)/([^/]+)"
    match = re.search(pattern, repo_url)

    if not match:
        raise ValueError("Invalid GitHub repository URL.")

    owner = match.group(1)
    repo = match.group(2).replace(".git", "")

    return owner, repo


def download_github_repo_zip(repo_url: str, destination_path: str):
    """
    Prenese javni GitHub repozitorij kot ZIP.
    Za začetek podpiramo samo public repos.
    """
    owner, repo = parse_github_url(repo_url)

    zip_url = f"https://api.github.com/repos/{owner}/{repo}/zipball"

    response = requests.get(zip_url, allow_redirects=True, timeout=30)

    if response.status_code != 200:
        raise ValueError(
            f"Could not download GitHub repository. Status code: {response.status_code}"
        )

    with open(destination_path, "wb") as file:
        file.write(response.content)


def extract_zip(zip_path: str, extract_dir: str):
    """
    Razširi preneseni GitHub ZIP v začasno source mapo.
    """
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)