import * as React from "react";
import { isAxiosError } from "axios";

import {useState} from "react";
import {useNavigate} from "react-router-dom";
import {Button} from "@/components/ui/button";
import {Input} from "@/components/ui/input";
import {Label} from "@/components/ui/label";
import {Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle} from "@/components/ui/card";
import {ArrowLeft, Bot} from "lucide-react";

import {AuthService} from "@/features/auth/services/authService"
import {useAuthStore} from "@/store/authStore.ts";
import type {LoginRequest} from "@/features/auth/auth";

import "@/features/auth/ui/LoginForm.css";


export default function LoginForm() {
  const navigate = useNavigate();

  const [isLoading, setIsLoading] = useState(false);

  // Auth state
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const setAuth = useAuthStore((state) => state.setAuth);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null)

    try {
      const credentials: LoginRequest = {
        "username": username,
        "password": password
      }

      const data = await AuthService.login(credentials);
      setAuth(data.jwt_token);
      console.log("Login successful:", data);

      navigate('/home');
    } catch (err: unknown) {
      console.error("Login failed:", err);
      let errorMessage = "Login failed. Please check your credentials.";

      if (isAxiosError(err)) {
        errorMessage = err.response?.data?.message || errorMessage;
      }

      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
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

        {error && (
          <div className="p-3 text-sm text-destructive bg-destructive/10">
            {error}
          </div>
        )}

        <CardContent>
          <form onSubmit={handleSubmit} className="login-form">
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                type="email"
                placeholder="example@email.com"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="********"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />
              <p className="authInputHint">
                Must be at least 8 characters including uppercase, lowercase, number and special character.
              </p>
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