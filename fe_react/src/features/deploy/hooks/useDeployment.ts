import { useState } from "react";
import { DeploymentService } from "@/features/deploy/service/deployService";
import { isAxiosError } from "axios";

export const useDeployment = () => {
  const [code, setCode] = useState(
    "// Write your Discord bot command logic here...\n\nclient.on('messageCreate', (message) => {\n  if (message.content === '!ping') {\n    message.reply('Pong!');\n  }\n});"
  );
  const [response, setResponse] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setResponse(null);

    try {
      const data = await DeploymentService.deploy({
        workflow_name: "discord_bot", // Default name for now
        script_content: code,
      });

      setResponse(
        `Successfully updated bot logic at ${new Date().toLocaleTimeString()}\n\n` +
        `Deployment Status: ${data.status}\n` +
        `Workflow: ${data.data.name}\n` +
        `Message: ${data.message}`
      );
    } catch (err: unknown) {
      console.error("Deployment failed:", err);
      let errorMessage = "Deployment failed. Please try again.";

      if (isAxiosError(err)) {
        if (err.code === "ECONNABORTED") {
          errorMessage = "The connection timed out. Please try again later.";
        } else if (!err.response) {
          errorMessage = "No response from server. Please check your internet connection.";
        } else {
          errorMessage = err.response?.data?.message || err.response?.data?.detail || errorMessage;
        }
      }
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
