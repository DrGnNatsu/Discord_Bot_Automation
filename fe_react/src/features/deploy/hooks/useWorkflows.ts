import { useState, useEffect, useCallback } from "react";
import toast from "react-hot-toast";
import { DeploymentService } from "../service/deployService";
import type { Workflow } from "../workflow";

export const useWorkflows = () => {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchWorkflows = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await DeploymentService.getWorkflows();
      setWorkflows(data);
    } catch (error) {
      console.error("Failed to fetch workflows:", error);
      toast.error("Failed to load workflows");
    } finally {
      setIsLoading(false);
    }
  }, []);

  const deleteWorkflow = async (id: string) => {
    try {
      await DeploymentService.deleteWorkflow(id);
      toast.success("Workflow deleted successfully");
      await fetchWorkflows(); // Refresh list
    } catch (error) {
      console.error("Failed to delete workflow:", error);
      toast.error("Failed to delete workflow");
    }
  };

  useEffect(() => {
    fetchWorkflows();
  }, [fetchWorkflows]);

  return {
    workflows,
    isLoading,
    fetchWorkflows,
    deleteWorkflow,
  };
};
