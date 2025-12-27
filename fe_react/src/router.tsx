import LandingPage from "@/app/LandingPage";
import Layout from "@/app/_layout";
import LoginPage from "@/app/auth/LoginPage";
import DashboardPage from "@/app/dashboard/DashboardPage";
import ProtectedRoute from "@/components/ProtectedRoute";
import { DocumentationPage } from "@/features/documentation";
import { createBrowserRouter } from "react-router-dom";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout,
    children: [
      {
        path: "",
        Component: LandingPage,
      },
      {
        path: "login",
        Component: LoginPage,
      },
      {
        path: "dashboard",
        element: (
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        )
      },
      {
        path: "docs",
        element: (
          <ProtectedRoute>
            <DocumentationPage />
          </ProtectedRoute>
        )
      }
    ],
  },
]);
