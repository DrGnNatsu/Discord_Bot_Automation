from typing import Dict, Any

from sqlalchemy.orm import Session

from app.models import Workflow


class WorkflowRepository:
    def __init__(self):
        pass

    def get_workflow_by_name(self, db: Session, name: str) -> Workflow | None:
        """Get workflow by name."""
        return db.query(Workflow).filter(Workflow.name == name).first()

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