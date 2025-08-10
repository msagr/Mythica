import uuid 
from typing import Optional 
from datetime import datetime 
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session 

from backend.db.database import get_db, SessionLocal 
from backend.models.story import Story, StoryNode 
from backend.models.job import StoryJob 
from backend.schema.story import (
    CompleteStoryResponse, CompleteStoryNodeResponse, CreateStoryRequest
) 
from backend.schema.job import StoryJobResponse 

# Organising story specific routes
# backend URL -> backendURL/api/stories
router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id 

@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())
    job = StoryJob(
        job_id=job_id,
        session_id = session_id,
        theme=request.theme, 
        status="pending"
    )

    db.add(job)
    db.commit()

    # TODO: add background tasks, generate story

    return job

