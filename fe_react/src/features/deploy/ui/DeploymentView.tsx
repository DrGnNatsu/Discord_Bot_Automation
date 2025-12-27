import {ResizableHandle, ResizablePanel, ResizablePanelGroup} from "@/components/ui/resizable";
import CodeEditor from "./CodeEditor";
import ResponsePanel from "./ResponsePanel";
import WorkflowList from "./WorkflowList";
import {useDeployment} from "../hooks/useDeployment";
import {useWorkflows} from "../hooks/useWorkflows";
import "./DeploymentView.css";

export default function DeploymentView() {
  const { workflows, isLoading: isWorkflowsLoading, fetchWorkflows, deleteWorkflow } = useWorkflows();
  const {code, setCode, response, isSubmitting, handleSubmit} = useDeployment(fetchWorkflows);

  return (
    <div className="deployment-view-container">
      <ResizablePanelGroup
        orientation="horizontal"
        className="deployment-panel-group"
      >
        {/* Left Side: Monaco Editor */}
        <ResizablePanel defaultSize={60} minSize={30}>
          <CodeEditor
            code={code}
            setCode={setCode}
            onSubmit={handleSubmit}
            isSubmitting={isSubmitting}
          />
        </ResizablePanel>

        <ResizableHandle withHandle />

        {/* Right Side: Response Output */}
        <ResizablePanel defaultSize={40} minSize={20}>
          <ResponsePanel response={response} />
        </ResizablePanel>
      </ResizablePanelGroup>

      <div className="flex flex-col gap-4">
        <h2 className="text-xl font-bold tracking-tight">Deployed Workflows</h2>
        <WorkflowList 
          workflows={workflows} 
          isLoading={isWorkflowsLoading} 
          onDelete={deleteWorkflow} 
        />
      </div>
    </div>
  );
};
