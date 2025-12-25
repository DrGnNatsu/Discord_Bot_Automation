import {create} from 'zustand';
import {persist} from 'zustand/middleware';
import type {AuthState} from '@/features/auth/auth';

interface AuthStore extends AuthState {
  setAuth: (jwt_token: string) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      jwt_token: null,
      isAuthenticated: false,
      setAuth: (jwt_token) => set({jwt_token, isAuthenticated: true}),
      clearAuth: () => set({jwt_token: null, isAuthenticated: false}),
    }),
    {
      name: 'auth-storage',
    }
  )
);