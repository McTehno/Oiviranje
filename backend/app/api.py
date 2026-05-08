import os
import json
import uuid
import zipfile
import shutil
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from pydantic import BaseModel
from app.github_utils import download_github_repo_zip, extract_zip

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from pipeline.project_analyzer import ProjectAnalyzer

app = FastAPI(title="SAST Analyzer API")
BACKEND_ROOT = Path(__file__).resolve().parents[1]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    # ZIP analiza tece v začasnem delovnem prostoru pod backendom,
    # zato ne uporablja Windows temp mape.
    with TemporaryDirectory(prefix="sast_zip_", dir=str(BACKEND_ROOT)) as temp_root:
        scan_dir = Path(temp_root)
        extract_dir = scan_dir / "source"

        if not project.filename or not project.filename.endswith(".zip"):
            return {
                "error": "Only ZIP project upload is supported."
            }

        extract_dir.mkdir(parents=True, exist_ok=True)

        zip_bytes = await project.read()

        with zipfile.ZipFile(BytesIO(zip_bytes), "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        parsed_database_config = json.loads(database_config)

        analyzer = ProjectAnalyzer()
        result = analyzer.analyze_project(
            project_path=str(extract_dir),
            database_config=parsed_database_config
        )

        result["scan_id"] = scan_id
        result["source"] = "zip"

        with open(scan_dir / "report.json", "w", encoding="utf-8") as file:
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
    # Folder analiza uporablja enako backend-local začasno delovno okolje kot ZIP analiza.
    with TemporaryDirectory(prefix="sast_folder_", dir=str(BACKEND_ROOT)) as temp_root:
        scan_dir = Path(temp_root)
        source_dir = scan_dir / "source"

        source_dir.mkdir(parents=True, exist_ok=True)

        parsed_database_config = json.loads(database_config)

        for uploaded_file in files:
            relative_path = uploaded_file.filename
            safe_path = os.path.normpath(relative_path)

            # osnovna zaščita pred pisanjem izven source_dir
            if safe_path.startswith(".."):
                continue

            destination_path = source_dir / safe_path
            destination_path.parent.mkdir(parents=True, exist_ok=True)

            with open(destination_path, "wb") as buffer:
                shutil.copyfileobj(uploaded_file.file, buffer)

        analyzer = ProjectAnalyzer()
        result = analyzer.analyze_project(
            project_path=str(source_dir),
            database_config=parsed_database_config
        )

        result["scan_id"] = scan_id
        result["source"] = "folder"

        with open(scan_dir / "report.json", "w", encoding="utf-8") as file:
            json.dump(result, file, indent=2)

        return result



@app.post("/analyze-github")
async def analyze_github(request: GitHubAnalyzeRequest):
    scan_id = str(uuid.uuid4())
    # GitHub analiza uporablja backend-local začasni workspace in zip izvede v spominu.
    with TemporaryDirectory(prefix="sast_github_", dir=str(BACKEND_ROOT)) as temp_root:
        scan_dir = Path(temp_root)
        extract_dir = scan_dir / "source"

        extract_dir.mkdir(parents=True, exist_ok=True)

        try:
            zip_bytes = download_github_repo_zip(repo_url=request.repo_url)

            extract_zip(zip_bytes, str(extract_dir))

            analyzer = ProjectAnalyzer()
            result = analyzer.analyze_project(
                project_path=str(extract_dir),
                database_config=request.database_config
            )

            result["scan_id"] = scan_id
            result["source"] = "github"
            result["repo_url"] = request.repo_url

            with open(scan_dir / "report.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=2)

            return result

        except Exception as error:
            return {
                "error": str(error)
            }