from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class ActionSchema(BaseModel):
    type: str = "ACTION"
    command: str
    params: Dict[str, Any] = {}

class TransitionSchema(BaseModel):
    type: str = "TRANSITION"
    target_state: str

class SetVarSchema(BaseModel):
    type: str = "SET_VAR"
    variable: str
    value: Any

class ComponentSchema(BaseModel):
    type: str = "UI_COMPONENT"
    component_type: str
    props: Dict[str, Any] = {}

class IfBlockSchema(BaseModel):
    type: str = "LOGIC_IF"
    condition: Dict[str, Any]
    then_branch: List[Any] = [] # List of steps
    else_branch: List[Any] = []

class StateSchema(BaseModel):
    type: str = "STATE"
    name: str
    steps: List[Any] = []

class WorkflowSchema(BaseModel):
    type: str = "WORKFLOW"
    name: str
    trigger: str
    condition: Optional[Dict[str, Any]] = None
    steps: List[Any] = []