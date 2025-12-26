import {ResizableHandle, ResizablePanel, ResizablePanelGroup} from "@/components/ui/resizable";
import CodeEditor from "./CodeEditor";
import ResponsePanel from "./ResponsePanel";
import {useDeployment} from "../hooks/useDeployment";
import "./DeploymentView.css";

export default function DeploymentView() {
  const {code, setCode, response, isSubmitting, handleSubmit} = useDeployment();

  return (
    <div className="deployment-view-container">
      <ResizablePanelGroup
        direction="horizontal"
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
    </div>
  );
};
