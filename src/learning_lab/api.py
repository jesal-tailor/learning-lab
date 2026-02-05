import logging
import os
import uuid
import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Request

from learning_lab.summarise_csv import summarise_csv

# Logging setup
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(message)s")
logger = logging.getLogger("learning_lab")

app = FastAPI(title="Learning Lab CSV Summariser")

APP_VERSION = "v1.0.1"

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(
        f'{{"request_id":"{request.state.request_id}","method":"{request.method}","path":"{request.url.path}","status":{response.status_code}}}'
    )
    return response


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"status": "ready"}

@app.get("/version")
def version():
    return {"version": os.getenv("RENDER_GIT_COMMIT", "unknown")}

@app.post("/summarise")
async def summarise(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / file.filename
        content = await file.read()
        tmp_path.write_bytes(content)

        report = summarise_csv(tmp_path)

    return {"filename": file.filename, "report": report}
