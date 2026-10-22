
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Project, Experiment
from app.schemas import ProjectInput, ProjectOut
from app.security import get_current_user, get_db

router = APIRouter(tags=["projects"])


@router.get("/projects", response_model=list[ProjectOut])
def list_projects(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(
        select(Project).where(Project.user_id == user.id).order_by(Project.id)
    ).all()


@router.post("/projects", response_model=ProjectOut, status_code=201)
def create_project(
    data: ProjectInput,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = Project(user_id=user.id, **data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.scalar(
        select(Project).where(Project.id == project_id, Project.user_id == user.id)
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")
    return project


@router.put("/projects/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    data: ProjectInput,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.scalar(
        select(Project).where(Project.id == project_id, Project.user_id == user.id)
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")

    for field, value in data.model_dump().items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)
    return project


@router.delete("/projects/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.scalar(
        select(Project).where(Project.id == project_id, Project.user_id == user.id)
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")

    experiments_count = db.scalar(
        select(func.count())
        .select_from(Experiment)
        .where(Experiment.project_id == project.id)
    )
    if experiments_count:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar un proyecto que contiene experimentos.",
        )

    db.delete(project)
    db.commit()
    return Response(status_code=204)
