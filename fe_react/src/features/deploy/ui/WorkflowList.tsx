import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";
import type { Workflow } from "../workflow";
import Editor from "@monaco-editor/react";
import { useThemeStore } from "@/store/themeStore";

interface WorkflowListProps {
  workflows: Workflow[];
  isLoading: boolean;
  onDelete: (id: string) => void;
}

export default function WorkflowList({ workflows, isLoading, onDelete }: WorkflowListProps) {
  const [selectedWorkflow, setSelectedWorkflow] = useState<Workflow | null>(null);
  const { isDarkMode } = useThemeStore();

  const handleRowClick = (workflow: Workflow) => {
    setSelectedWorkflow(workflow);
  };

  if (isLoading) {
    return <div className="p-4 text-center text-muted-foreground">Loading workflows...</div>;
  }

  if (workflows.length === 0) {
    return <div className="p-8 text-center text-muted-foreground border rounded-md border-dashed">No workflows deployed yet.</div>;
  }

  return (
    <>
      <div className="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Trigger</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Last Updated</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {workflows.map((workflow) => (
              <TableRow 
                key={workflow.id} 
                className="cursor-pointer hover:bg-muted/60"
                onClick={() => handleRowClick(workflow)}
              >
                <TableCell className="font-medium">{workflow.name}</TableCell>
                <TableCell>
                  <code className="bg-muted px-1.5 py-0.5 rounded text-xs font-mono">
                    {workflow.trigger_event}
                  </code>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <span className={`size-2 rounded-full ${workflow.is_active ? 'bg-green-500' : 'bg-gray-300'}`} />
                    {workflow.is_active ? 'Active' : 'Inactive'}
                  </div>
                </TableCell>
                <TableCell className="text-muted-foreground text-sm">
                  {new Date(workflow.updated_at).toLocaleString()}
                </TableCell>
                <TableCell className="text-right">
                  <Button
                    variant="ghost"
                    size="sm"
                    className="text-destructive hover:bg-destructive/10 hover:text-destructive h-8 w-8 p-0"
                    onClick={(e) => {
                      e.stopPropagation();
                      if (confirm("Are you sure you want to delete this workflow? This action cannot be undone.")) {
                        onDelete(workflow.id);
                      }
                    }}
                  >
                    <Trash2 className="size-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <Dialog open={!!selectedWorkflow} onOpenChange={(open) => !open && setSelectedWorkflow(null)}>
        <DialogContent className="max-w-3xl max-h-[80vh] flex flex-col">
          <DialogHeader>
            <DialogTitle>{selectedWorkflow?.name}</DialogTitle>
            <DialogDescription>
              Trigger: {selectedWorkflow?.trigger_event} | ID: {selectedWorkflow?.id}
            </DialogDescription>
          </DialogHeader>
          <div className="h-[500px] w-full border rounded-md overflow-hidden">
             <Editor
              height="100%"
              defaultLanguage="plaintext"
              theme={isDarkMode ? "vs-dark" : "light"}
              value={selectedWorkflow?.source_code || "// No source code available"}
              options={{
                readOnly: true,
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: "on",
                scrollBeyondLastLine: false,
                automaticLayout: true,
                padding: { top: 16 },
                wordWrap: "on",
              }}
            />
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}
