export const API_ENDPOINTS_V1 = {
  AUTH: {
    LOGIN: `/v1/auth/login`,
  },
  DEPLOYMENT: {
    DEPLOY: `/v1/deploy`,
    LIST_WORKFLOWS: `/v1/deploy/workflows`,
    DELETE_WORKFLOW: (workflowId: string) => `/v1/deploy/workflows/${workflowId}`,
  }
}