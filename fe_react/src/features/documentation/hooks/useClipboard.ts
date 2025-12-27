import { useCallback, useState } from "react";
import toast from "react-hot-toast";

export const useClipboard = () => {
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const copyToClipboard = useCallback(async (text: string, id: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedId(id);
      toast.success("Copied to clipboard!", {
        duration: 2000,
        icon: "📋",
      });
      
      // Reset copied state after 2 seconds
      setTimeout(() => setCopiedId(null), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
      toast.error("Failed to copy to clipboard");
    }
  }, []);

  return {
    copiedId,
    copyToClipboard,
  };
};
