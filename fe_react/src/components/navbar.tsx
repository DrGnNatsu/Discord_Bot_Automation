import ThemeToggle from "@/components/theme-toggle.tsx"
import {Bot, Monitor} from "lucide-react";
import {Button} from "@/components/ui/button.tsx";
import { useNavigate } from "react-router-dom";
import "@/components/css/navbar.css"
import {useAuthStore} from "@/store/authStore.ts";

export default function Navbar() {
  const navigate = useNavigate();
  const isAuthenticated = useAuthStore(state => state.isAuthenticated)
  const clearAuthStorage = useAuthStore(state => state.clearAuth)

  const handleLogout = () => {
    clearAuthStorage();
    navigate("/");
  }

  return (
    <>
      <nav>
        <div className="navContainer">
          <div className="layoutNavbar">
            {/* Left - Logo and Brand */}
            <div className="leftNavbar" onClick={() => navigate("/")}>
              <Bot className="iconBot" />
              <span>Bot Admin Dashboard</span>
            </div>

            {isAuthenticated && (
              <div className="midNavbar" onClick={() => navigate("/dashboard")}>
                <Monitor className="iconBot_small" />
                <span>Dashboard</span>
              </div>
            )}

            {/* Right - Theme Toggle and Login */}
            <div className="rightNavbar">
              <ThemeToggle />
              {!isAuthenticated ?
                (<Button onClick={() => navigate("/login")}>Login</Button>)
                :
                (<Button variant="destructive" onClick={handleLogout}>Logout</Button>)
              }

            </div>
          </div>
        </div>
      </nav>
    </>
  )
}