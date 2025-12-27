import "@/components/css/navbar.css";
import ThemeToggle from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/store/authStore";
import { Book, Bot, Monitor } from "lucide-react";
import { useNavigate } from "react-router-dom";

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
              <div className="midNavbar">
                <div className="navItem" onClick={() => navigate("/dashboard")}>
                  <Monitor className="iconBot_small" />
                  <span>Dashboard</span>
                </div>
                <div className="navItem" onClick={() => navigate("/docs")}>
                  <Book className="iconBot_small" />
                  <span>Docs</span>
                </div>
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