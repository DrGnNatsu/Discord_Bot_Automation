import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, Bot } from "lucide-react";
import "@/features/auth/ui/LoginForm.css";

export default function LoginForm() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
      console.log("Login attempted");
    }, 1500);
  };

  return (
    <div className="login-container">
      <Card className="login-card">
        <CardHeader className="space-y-1">
          <div className="flex justify-center mb-4">
            <Bot className="size-10 text-primary" />
          </div>
          <CardTitle className="text-2xl text-center">Welcome back</CardTitle>
          <CardDescription className="text-center">
            Enter your credentials to access your dashboard
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="login-form">
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input id="username" placeholder="natsu" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" required />
            </div>
            <Button className="w-full" type="submit" disabled={isLoading}>
              {isLoading ? "Signing in..." : "Sign In"}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <div className="login-footer">
            Don&apos;t have an account?{" "}
            <span className="text-primary hover:underline cursor-pointer font-medium">
              Contact Admin
            </span>
          </div>
          <div 
            className="back-link"
            onClick={() => navigate("/")}
          >
            <ArrowLeft className="size-4" />
            <span>Back to Landing Page</span>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}