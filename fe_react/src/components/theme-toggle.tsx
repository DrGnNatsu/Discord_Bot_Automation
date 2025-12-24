import {Switch} from "@/components/ui/switch"
import {Label} from "@/components/ui/label"
import {useThemeStore} from "@/store/themeStore";
import {Moon, Sun} from "lucide-react";
import {useEffect} from "react";

export default function ThemeToggle() {
  const {isDarkMode, toggleTheme, initTheme} = useThemeStore()

  useEffect (() => {
    initTheme()
  }, [initTheme])

  const handleToggleTheme = (checked: boolean) => {
    toggleTheme(checked)
  }

  return (
    <div className="flex items-center gap-4 p-4 border rounded-lg bg-card">
      <div className="flex items-center gap-2">
        <Switch 
          id="theme-toggle"
          checked={isDarkMode} 
          onCheckedChange={handleToggleTheme} 
        />
        <Label htmlFor="theme-toggle" className="cursor-pointer">
          {isDarkMode ? "Dark Mode" : "Light Mode"}
        </Label>
      </div>
      <div className="flex items-center justify-center w-8 h-8">
        {isDarkMode ? (
          <Moon className="w-5 h-5 text-primary" />
        ) : (
          <Sun className="w-5 h-5 text-orange-500" />
        )}
      </div>
    </div>
  )
}