import {axiosInstance} from "@/api/axiosInstance";
import { API_ENDPOINTS_V1 } from "@/constants/api";

import type {DeploymentRequest, DeploymentResponse, Workflow} from "@/features/deploy/workflow"

export const DeploymentService = {
  deploy: async ({workflow_name, script_content}: DeploymentRequest): Promise<DeploymentResponse> => {
    const response = await axiosInstance.post<DeploymentResponse>(API_ENDPOINTS_V1.DEPLOYMENT.DEPLOY, {
      workflow_name,
      script_content,
    });
    return response.data;
  },

  getWorkflows: async (): Promise<Workflow[]> => {
    const response = await axiosInstance.get<Workflow[]>(API_ENDPOINTS_V1.DEPLOYMENT.LIST_WORKFLOWS);
    return response.data;
  },

  deleteWorkflow: async (workflowId: string): Promise<void> => {
    await axiosInstance.delete(API_ENDPOINTS_V1.DEPLOYMENT.DELETE_WORKFLOW(workflowId));
  },
}