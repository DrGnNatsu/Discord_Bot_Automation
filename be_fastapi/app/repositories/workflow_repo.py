from typing import Dict, Any, List

from sqlalchemy.orm import Session

from app.models import Workflow, ActiveSession


class WorkflowRepository:
    def __init__(self):
        pass


    def get_all_workflow_by_trigger_event(self, db: Session, trigger_event:str) -> list[type[Workflow]]:
        return db.query(Workflow).filter(Workflow.trigger_event == trigger_event).all()
        
    def get_workflow_by_name(self, db: Session, name: str) -> Workflow | None:
        """Get workflow by name."""
        return db.query(Workflow).filter(Workflow.name == name).first()
        
    def get_workflow_by_id(self, db: Session, workflow_id: str) -> Workflow | None:
        """Get workflow by UUID."""
        return db.query(Workflow).filter(Workflow.id == workflow_id).first()

    def get_all_workflows(self, db: Session) -> List[Workflow]:
        """Get all workflows."""
        return db.query(Workflow).all()

    def create_workflow(
        self,
        db: Session,
        name: str,
        trigger_event: str,
        source_code: str,
        compiled_json: Dict[str, Any]
    ) -> Workflow:
        """Create a new workflow."""
        workflow = Workflow(
            name=name,
            trigger_event=trigger_event,
            source_code=source_code,
            compiled_json=compiled_json
        )
        db.add(workflow)
        return workflow

    def update_workflow(
        self,
        db: Session,
        workflow: Workflow,
        source_code: str,
        compiled_json: Dict[str, Any],
        trigger_event: str
    ) -> Workflow:
        """Update an existing workflow."""
        workflow.source_code = source_code
        workflow.compiled_json = compiled_json
        workflow.trigger_event = trigger_event
        return workflow

    def delete_workflow(self, db: Session, workflow: Workflow):
        """Delete a workflow."""
        db.delete(workflow)
        
    def delete_active_sessions_by_workflow(self, db: Session, workflow_id: str):
        """Cascade delete active sessions using this workflow."""
        db.query(ActiveSession).filter(ActiveSession.workflow_id == workflow_id).delete()
