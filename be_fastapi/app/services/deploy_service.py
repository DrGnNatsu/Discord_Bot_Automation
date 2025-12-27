import logging
from typing import Dict, Any, List

from sqlalchemy.orm import Session

from compiler.compiler import compile_code
from app.exception.deploy_exception import NoWorkflowFoundException, CompilationFailedException
from app.repositories.workflow_repo import WorkflowRepository
from app.schemas.deploy import DeploymentResponse

logger = logging.getLogger(__name__)


class DeployService:
    """Service for handling workflow deployment logic."""

    MESSAGES = {
        "updated": "Workflow updated successfully",
        "created": "Workflow created successfully",
    }

    def __init__(self, workflow_repo: WorkflowRepository):
        self.workflow_repo = workflow_repo

    def _extract_trigger_event(self, workflow_data: Dict[str, Any]) -> str:
        """Extract trigger event from compiled workflow data."""
        return workflow_data.get("trigger", "unknown")

    def _compile_script(self, script_content: str) -> List[Dict[str, Any]]:
        """
        Compile workflow script into JSON representation.
        
        Args:
            script_content: The workflow script to compile
            
        Returns:
            List of compiled workflow dictionaries
            
        Raises:
            CompilationFailedException: If compilation fails
            NoWorkflowFoundException: If no workflow found in script
        """
        try:
            compiled_workflows = compile_code(script_content)
            
            if not compiled_workflows:
                raise NoWorkflowFoundException()
                
            return compiled_workflows
        except NoWorkflowFoundException:
            raise
        except Exception as e:
            logger.error(f"Compilation error: {str(e)}", exc_info=True)
            raise CompilationFailedException(detail=str(e))

    def deploy_workflow(
        self,
        workflow_name: str,
        script_content: str,
        db: Session
    ) -> DeploymentResponse:
        """
        Deploy a workflow by compiling and saving to database.
        
        Args:
            workflow_name: Name of the workflow
            script_content: Script content to compile
            db: Database session
            
        Returns:
            DeploymentResponse with status and workflow data
            
        Raises:
            NoWorkflowFoundException: If no workflow found in script
            CompilationFailedException: If compilation fails
        """
        logger.info(f"Deployment initiated for workflow: {workflow_name}")

        # Compile the script
        compiled_workflows = self._compile_script(script_content)
        workflow_data = compiled_workflows[0]
        
        # Extract trigger event
        trigger_event = self._extract_trigger_event(workflow_data)
        
        # Check if workflow exists
        existing = self.workflow_repo.get_workflow_by_name(db, workflow_name)
        
        if existing:
            # Update existing workflow
            self.workflow_repo.update_workflow(
                db=db,
                workflow=existing,
                source_code=script_content,
                compiled_json=workflow_data,
                trigger_event=trigger_event
            )
            message = self.MESSAGES["updated"]
            logger.info(f"Workflow updated: {workflow_name}")
        else:
            # Create new workflow
            self.workflow_repo.create_workflow(
                db=db,
                name=workflow_name,
                trigger_event=trigger_event,
                source_code=script_content,
                compiled_json=workflow_data
            )
            message = self.MESSAGES["created"]
            logger.info(f"Workflow created: {workflow_name}")
        
        db.commit()
        logger.info(f"Deployment successful for workflow: {workflow_name}")

        return DeploymentResponse(
            status="success",
            message=message,
            data=workflow_data
        )
