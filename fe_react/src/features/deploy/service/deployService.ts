import {axiosInstance} from "@/api/axiosInstance";
import { API_ENDPOINTS_V1 } from "@/constants/api";

import type {DeploymentRequest, DeploymentResponse} from "@/features/deploy/workflow"

export const DeploymentService = {
  deploy: async ({workflow_name, script_content}: DeploymentRequest): Promise<DeploymentResponse> => {
    const response = await axiosInstance.post<DeploymentResponse>(API_ENDPOINTS_V1.DEPLOYMENT.DEPLOY, {
      workflow_name,
      script_content,
    });
    return response.data;
  },
}