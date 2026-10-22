
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Experiment, Project
from app.schemas import ExperimentInput, ExperimentOut
from app.security import get_current_user, get_db

router = APIRouter(tags=["experiments"])


@router.get("/projects/{project_id}/experiments", response_model=list[ExperimentOut])
def list_experiments(
    project_id: int,
    model: str | None = None,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.scalar(
        select(Project).where(Project.id == project_id, Project.user_id == user.id)
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")

    query = select(Experiment).where(Experiment.project_id == project_id)
    if model is not None:
        query = query.where(Experiment.model == model)

    return db.scalars(query.order_by(Experiment.id)).all()


@router.post(
    "/projects/{project_id}/experiments",
    response_model=ExperimentOut,
    status_code=201,
)
def create_experiment(
    project_id: int,
    data: ExperimentInput,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.scalar(
        select(Project).where(Project.id == project_id, Project.user_id == user.id)
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")

    experiment = Experiment(project_id=project.id, **data.model_dump())
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    return experiment


@router.get("/experiments/{experiment_id}", response_model=ExperimentOut)
def get_experiment(
    experiment_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    experiment = db.scalar(
        select(Experiment)
        .join(Project)
        .where(Experiment.id == experiment_id, Project.user_id == user.id)
    )
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experimento no encontrado.")
    return experiment


@router.put("/experiments/{experiment_id}", response_model=ExperimentOut)
def update_experiment(
    experiment_id: int,
    data: ExperimentInput,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    experiment = db.scalar(
        select(Experiment)
        .join(Project)
        .where(Experiment.id == experiment_id, Project.user_id == user.id)
    )
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experimento no encontrado.")

    for field, value in data.model_dump().items():
        setattr(experiment, field, value)

    db.commit()
    db.refresh(experiment)
    return experiment


@router.delete("/experiments/{experiment_id}", status_code=204)
def delete_experiment(
    experiment_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    experiment = db.scalar(
        select(Experiment)
        .join(Project)
        .where(Experiment.id == experiment_id, Project.user_id == user.id)
    )
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experimento no encontrado.")

    db.delete(experiment)
    db.commit()
    return Response(status_code=204)
