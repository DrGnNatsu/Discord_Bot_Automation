import {Send, Terminal} from "lucide-react";
import {ScrollArea} from "@/components/ui/scroll-area";
import {Card, CardContent, CardTitle} from "@/components/ui/card";


interface ResponsePanelProps {
  response: string | null;
}

export default function ResponsePanel({response}: ResponsePanelProps) {

  return (
    <Card className="border-0 rounded-none h-full flex flex-col shadow-none bg-card p-0">
      <div className="deployment-header">
        <div className="flex items-center gap-2">
          <Send className="size-4 text-primary" />
          <CardTitle className="text-sm font-bold">Response Output</CardTitle>
        </div>
      </div>
      <CardContent className="flex-1 p-0 overflow-hidden relative">
        <ScrollArea className="h-full">
          <div className="p-4 font-mono text-sm">
            {response ? (
              <pre
                className={`whitespace-pre-wrap ${response.startsWith('ERROR') ? 'error-text' : 'success-text'}`}>
                {response}
              </pre>
            ) : (
              <div className="flex flex-col items-center justify-center h-full py-20 text-muted-foreground opacity-50">
                <Terminal className="size-12 mb-4" />
                <p>Awaiting submission...</p>
                <p className="text-xs">Click "Submit Code" to see the output</p>
              </div>
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
