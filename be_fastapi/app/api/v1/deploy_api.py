import logging

from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exception.deploy_exception import NoWorkflowFoundException, CompilationFailedException
from app.schemas.deploy import DeployRequest, DeploymentResponse
from app.services.deploy_service import DeployService
from app.api.v1.depends import get_current_user, get_deploy_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/deploy", tags=["Deploy"])


@router.post("", response_model=DeploymentResponse, status_code=status.HTTP_200_OK)
async def deploy_workflow(
    payload: DeployRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
    deploy_service: DeployService = Depends(get_deploy_service)
):
    """
    Deploy a workflow by compiling the script and saving it to the database.
    
    Args:
        payload: Deployment request containing workflow name and script content
        db: Database session
        user_id: Authenticated user ID
        deploy_service: Deploy service instance
        
    Returns:
        DeploymentResponse with status, message, and compiled workflow data
        
    Raises:
        HTTPException: If compilation fails or no workflow found
    """
    try:
        return deploy_service.deploy_workflow(
            workflow_name=payload.workflow_name,
            script_content=payload.script_content,
            db=db
        )
    except NoWorkflowFoundException as e:
        logger.warning(f"No workflow found for: {payload.workflow_name}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except CompilationFailedException as e:
        logger.error(f"Compilation failed for: {payload.workflow_name}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Deployment failed for {payload.workflow_name}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to deploy workflow: {str(e)}"
        )
