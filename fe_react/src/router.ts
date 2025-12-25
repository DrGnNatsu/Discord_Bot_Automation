import { createBrowserRouter } from "react-router-dom";
import LandingPage from "@/app/LandingPage";
import LoginPage from "@/app/auth/LoginPage";
import Layout from "@/app/_layout";

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
    ],
  },
]);
