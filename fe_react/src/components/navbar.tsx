import ThemeToggle from "@/components/theme-toggle.tsx"
import {Bot} from "lucide-react";
import {Button} from "@/components/ui/button.tsx";
import "@/components/css/navbar.css"
export default function Navbar() {
  return (
    <>
      <nav>
        <div className="navContainer">
          <div className="layoutNavbar">
            {/* Left - Logo and Brand */}
            <div className="leftNavbar">
              <Bot className="iconBot" />
              <span>Bot Admin Dashboard</span>
            </div>

            {/* Right - Theme Toggle and Login */}
            <div className="rightNavbar">
              <ThemeToggle />
              <Button>Login</Button>
            </div>
          </div>
        </div>
      </nav>
    </>
  )
}