import Navbar from "@/components/navbar";
import DeploymentView from "@/features/deploy/ui/DeploymentView";

export default function DashboardPage() {
  return (
    <div className="flex flex-col h-screen bg-background">
      <Navbar />
      <main className="flex-1 overflow-hidden p-4 md:p-6">
        <DeploymentView />
      </main>
    </div>
  );
}