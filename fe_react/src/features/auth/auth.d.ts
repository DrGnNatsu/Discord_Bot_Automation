export interface LoginResponse {
    jwt_token: string;
    token_type: string;
}

export interface LoginRequest {
    username: string;
    password: string;
}

export interface AuthState {
    jwt_token: string | null;
    isAuthenticated: boolean;
}