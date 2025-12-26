from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DeployRequest(BaseModel):
    workflow_name: str
    script_content: str
    admin_id: str

# 1. The smallest unit: An Action
class ActionModel(BaseModel):
    type: str              # e.g., "ACTION"
    command: str           # e.g., "SEND_MESSAGE"
    # We use Dict[str, Any] because params change based on command (some have int, some str)
    params: Dict[str, Any] 

# 2. The Core Data: The Workflow Logic
class WorkflowDataModel(BaseModel):
    type: str              # e.g., "WORKFLOW"
    name: str              # e.g., "mock_workflow"
    trigger: str           # e.g., "message"
    filter: Optional[Dict[str, Any]] = None  # Can be None or a filter object
    actions: List[ActionModel]

# 3. The API Response Wrapper
class DeploymentResponse(BaseModel):
    status: str            # "success" or "error"
    message: str           # Human readable message
    data: WorkflowDataModel
