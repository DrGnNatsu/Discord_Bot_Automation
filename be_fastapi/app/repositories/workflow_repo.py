from sqlalchemy.orm import Session

from app.models import Workflow


class WorkflowRepository:
    def __init__(self):
        pass

    def get_workflow_by_name(self, db: Session, name:str) -> Workflow | None:
        return db.query(Workflow).filter(Workflow.name == name).first()