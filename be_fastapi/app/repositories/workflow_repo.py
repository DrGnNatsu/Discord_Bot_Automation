from sqlalchemy.orm import Session

from app.models import Workflow


class WorkflowRepository:
    def __init__(self):
        pass

    def get_workflow_by_name(self, db: Session, name:str) -> Workflow | None:
        return db.query(Workflow).filter(Workflow.name == name).first()

    def get_all_workflow_by_trigger_event(self, db: Session, trigger_event:str) -> list[type[Workflow]]:
        return db.query(Workflow).filter(Workflow.trigger_event == trigger_event).all()