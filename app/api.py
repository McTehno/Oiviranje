import os
import json
import uuid
import zipfile
import shutil

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