export interface DeploymentRequest {
  workflow_name: string;
  script_content: string;
}

export interface DeploymentResponse {
  status: "success" | "error";
  message: string;
  data: WorkflowData;
}

export interface Action {
  type: string;
  command: string;
  // Record<string, any> allows dynamic keys like 'channel', 'duration', etc.
  params: Record<string, any>;
}

// 2. The Core Data: The Workflow Logic
export interface WorkflowData {
  type: string;
  name: string;
  trigger: string;
  // It can be a complex object or null
  filter: Record<string, any> | null;
  actions: Action[];
}