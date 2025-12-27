import { DeploymentService } from "@/features/deploy/service/deployService";
import { isAxiosError } from "axios";
import { useState } from "react";
import toast from "react-hot-toast";

// Default GuildFlow DSL template
const DEFAULT_CODE = `// GuildFlow DSL - Write your workflow here
// Visit the Documentation page for syntax examples

WORKFLOW my_workflow ON message {
    ACTION: REPLY_MESSAGE content="Hello from GuildFlow!"
}`;

export const useDeployment = () => {
  const [code, setCode] = useState(DEFAULT_CODE);
  const [response, setResponse] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setResponse(null);

    // Show loading toast
    const loadingToast = toast.loading("Deploying workflow...");

    try {
      const data = await DeploymentService.deploy({
        workflow_name: "discord_bot",
        script_content: code,
      });

      // Dismiss loading toast and show success
      toast.dismiss(loadingToast);
      toast.success(`✅ Workflow '${data.data.name}' deployed successfully!`, {
        duration: 5000,
      });

      setResponse(
        `Successfully deployed at ${new Date().toLocaleTimeString()}\n\n` +
        `Status: ${data.status}\n` +
        `Workflow: ${data.data.name}\n` +
        `Trigger: ${data.data.trigger}\n` +
        `Message: ${data.message}`
      );
    } catch (err: unknown) {
      console.error("Deployment failed:", err);
      
      // Dismiss loading toast
      toast.dismiss(loadingToast);

      let errorMessage = "Deployment failed. Please try again.";

      if (isAxiosError(err)) {
        if (err.code === "ECONNABORTED") {
          errorMessage = "The connection timed out. Please try again later.";
        } else if (!err.response) {
          errorMessage = "No response from server. Please check your internet connection.";
        } else {
          // Extract detailed error message
          const detail = err.response?.data?.detail;
          if (typeof detail === "string") {
            // Check if it contains line information for syntax errors
            if (detail.includes("Line")) {
              errorMessage = `❌ Syntax Error: ${detail}`;
            } else {
              errorMessage = detail;
            }
          } else {
            errorMessage = err.response?.data?.message || errorMessage;
          }
        }
      }

      // Show error toast
      toast.error(errorMessage, {
        duration: 6000,
      });

      setResponse(`ERROR: ${errorMessage}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return {
    code,
    setCode,
    response,
    isSubmitting,
    handleSubmit,
  };
};
