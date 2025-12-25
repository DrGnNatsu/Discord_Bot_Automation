import {Switch} from "@/components/ui/switch"
import {Label} from "@/components/ui/label"
import {useThemeStore} from "@/store/themeStore";
import {Moon, Sun} from "lucide-react";
import {useEffect} from "react";
import "@/components/css/theme-toggle.css"

export default function ThemeToggle() {
  const {isDarkMode, toggleTheme, initTheme} = useThemeStore()

  useEffect(() => {
    initTheme()
  }, [initTheme])

  const handleToggleTheme = (checked: boolean) => {
    toggleTheme(checked)
  }

  return (
    <>
      <div className="themeContainer">
        <Switch
          id="theme-toggle"
          checked={isDarkMode}
          onCheckedChange={handleToggleTheme}
          className="scale-125"
        />

        {/* Label */}
        <Label htmlFor="theme-toggle" className="cursor-pointer">
          {isDarkMode ?
            <div className="theme-toggle-label">
              <p>Dark Mode</p>
              <Moon className="iconTheme text-primary" />
            </div>
            :
            <div className="theme-toggle-label">
              <p>Light Mode</p>
              <Sun className="iconTheme text-orange-500" />
            </div>
          }
        </Label>

      </div>
    </>

  )
}