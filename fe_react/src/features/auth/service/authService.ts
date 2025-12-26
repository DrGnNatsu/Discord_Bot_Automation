import {axiosInstance} from "@/api/axiosInstance";
import { API_ENDPOINTS_V1 } from "@/constants/api";
import type {LoginRequest, LoginResponse} from "@/features/auth/auth"

export const AuthService = {
  login: async ({username, password}: LoginRequest): Promise<LoginResponse> => {
    const response = await axiosInstance.post<LoginResponse>(API_ENDPOINTS_V1.AUTH.LOGIN, {
      username,
      password,
    });
    return response.data;
  },
}