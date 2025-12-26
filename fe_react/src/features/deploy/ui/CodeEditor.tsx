import {Play, Terminal} from "lucide-react";
import {Button} from "@/components/ui/button";
import Editor from "@monaco-editor/react";
import {useThemeStore} from "@/store/themeStore";

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
          <span className="text-sm font-medium">BOT.dsl</span>
        </div>
        <Button
          size="sm"
          onClick={onSubmit}
          disabled={isSubmitting}
          className="gap-2"
        >
          {isSubmitting ? (
            <span
              className="animate-spin rounded-full h-3 w-3 border-2 border-primary-foreground border-t-transparent" />
          ) : (
            <Play className="size-3 fill-current" />
          )}
          Submit Code
        </Button>
      </div>
      <div className="flex-1 min-h-0">
        <Editor
          height="100%"
          defaultLanguage="javascript"
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
          }}
        />
      </div>
    </div>
  );
};
