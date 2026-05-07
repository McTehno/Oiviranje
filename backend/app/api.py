import os
import json
import uuid
import zipfile
import shutil

from pydantic import BaseModel
from app.github_utils import download_github_repo_zip, extract_zip

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from pipeline.project_analyzer import ProjectAnalyzer

app = FastAPI(title="SAST Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_ROOT = "uploaded_projects"

class GitHubAnalyzeRequest(BaseModel):
    repo_url: str
    database_config: dict

@app.get("/")
def root():
    return {
        "message": "SAST Analyzer API is running"
    }


@app.post("/analyze-project")
async def analyze_project(
    project: UploadFile = File(...),
    database_config: str = Form(...)
):
    scan_id = str(uuid.uuid4())
    scan_dir = os.path.join(UPLOAD_ROOT, scan_id)
    zip_path = os.path.join(scan_dir, project.filename)
    extract_dir = os.path.join(scan_dir, "source")

    os.makedirs(scan_dir, exist_ok=True)

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(project.file, buffer)

    if not project.filename.endswith(".zip"):
        return {
            "error": "Only ZIP project upload is supported."
        }

    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    parsed_database_config = json.loads(database_config)

    analyzer = ProjectAnalyzer()
    result = analyzer.analyze_project(
        project_path=extract_dir,
        database_config=parsed_database_config
    )

    result["scan_id"] = scan_id

    with open(os.path.join(scan_dir, "report.json"), "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)

    return result

# Ta endpoint omogoča analizo projekta, ki je naložen kot mapa. 
# Datoteka se razširi v začasno mapo, nato pa se izvede analiza. 
# Rezultati analize se shranijo v JSON datoteko in vrnejo kot odgovor.
@app.post("/analyze-folder")
async def analyze_folder(
        files: list[UploadFile] = File(...),
        database_config: str = Form(...)
):
    scan_id = str(uuid.uuid4())
    scan_dir = os.path.join(UPLOAD_ROOT, scan_id)
    source_dir = os.path.join(scan_dir, "source")

    os.makedirs(source_dir, exist_ok=True)

    parsed_database_config = json.loads(database_config)

    for uploaded_file in files:
        relative_path = uploaded_file.filename
        safe_path = os.path.normpath(relative_path)

        # osnovna zaščita pred pisanjem izven source_dir
        if safe_path.startswith(".."):
            continue

        destination_path = os.path.join(source_dir, safe_path)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        with open(destination_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)

    analyzer = ProjectAnalyzer()
    result = analyzer.analyze_project(
        project_path=source_dir,
        database_config=parsed_database_config
    )

    result["scan_id"] = scan_id
    result["source"] = "folder"

    with open(os.path.join(scan_dir, "report.json"), "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)

    return result



@app.post("/analyze-github")
async def analyze_github(request: GitHubAnalyzeRequest):
    scan_id = str(uuid.uuid4())
    scan_dir = os.path.join(UPLOAD_ROOT, scan_id)
    zip_path = os.path.join(scan_dir, "github_repo.zip")
    extract_dir = os.path.join(scan_dir, "source")

    os.makedirs(scan_dir, exist_ok=True)

    try:
        download_github_repo_zip(
            repo_url=request.repo_url,
            destination_path=zip_path
        )

        extract_zip(zip_path, extract_dir)

        analyzer = ProjectAnalyzer()
        result = analyzer.analyze_project(
            project_path=extract_dir,
            database_config=request.database_config
        )

        result["scan_id"] = scan_id
        result["source"] = "github"
        result["repo_url"] = request.repo_url

        with open(os.path.join(scan_dir, "report.json"), "w", encoding="utf-8") as file:
            json.dump(result, file, indent=2)

        return result

    except Exception as error:
        return {
            "error": str(error)
        }