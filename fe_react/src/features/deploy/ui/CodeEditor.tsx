import { Button } from "@/components/ui/button";
import { useThemeStore } from "@/store/themeStore";
import Editor from "@monaco-editor/react";
import { Loader2, Play, Terminal } from "lucide-react";

interface CodeEditorProps {
  code: string;
  setCode: (value: string) => void;
  onSubmit: () => void;
  isSubmitting: boolean;
}

export default function CodeEditor({
                                     code,
                                     setCode,
                                     onSubmit,
                                     isSubmitting,
                                   }: CodeEditorProps) {
  const {isDarkMode} = useThemeStore();

  return (
    <div className="flex flex-col h-full">
      <div className="deployment-header">
        <div className="flex items-center gap-2">
          <Terminal className="size-4 text-primary" />
          <span className="text-sm font-medium">workflow.gf</span>
        </div>
        <Button
          size="sm"
          onClick={onSubmit}
          disabled={isSubmitting}
          className="gap-2"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="size-3 animate-spin" />
              Deploying...
            </>
          ) : (
            <>
              <Play className="size-3 fill-current" />
              Deploy
            </>
          )}
        </Button>
      </div>
      <div className="flex-1 min-h-0">
        <Editor
          height="100%"
          defaultLanguage="plaintext"
          theme={isDarkMode ? "vs-dark" : "light"}
          value={code}
          onChange={(value) => setCode(value || "")}
          options={{
            minimap: {enabled: false},
            fontSize: 14,
            lineNumbers: "on",
            scrollBeyondLastLine: false,
            automaticLayout: true,
            padding: {top: 16},
            wordWrap: "on",
          }}
        />
      </div>
    </div>
  );
};
