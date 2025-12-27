from typing import List, Optional, Dict, Any

from pydantic import BaseModel

from app.enums.status import Status


# 1. The smallest unit: An Action
class ActionModel(BaseModel):
    type: str  # e.g., "ACTION"
    command: str  # e.g., "SEND_MESSAGE"
    # We use Dict[str, Any] because params change based on command (some have int, some str)
    params: Dict[str, Any]


# 2. The Core Data: The Workflow Logic
class WorkflowDataModel(BaseModel):
    type: str  # e.g., "WORKFLOW"
    name: str  # e.g., "mock_workflow"
    trigger: str  # e.g., "message"
    condition: Optional[Dict[str, Any]] = None 
    steps: List[Dict[str, Any]]  
    
class DeployRequest(BaseModel):
    workflow_name: Optional[str] = None
    script_content: str
    # admin_id: str


class DeploymentResponse(BaseModel):
    status: Status  # "success" or "error"
    message: str  # Readable message
    data: WorkflowDataModel
