import axios from "axios";

export const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 10000, // 10 seconds timeout
  headers: {
    "Content-type": "application/json",
  },
});

// interceptors: run before every request
axiosInstance.interceptors.request.use(
  (config) => {
    const authStorage = localStorage.getItem("auth-storage");
    if (authStorage) {
      try {
        const { state } = JSON.parse(authStorage);
        if (state && state.jwt_token) {
          config.headers.Authorization = `Bearer ${state.jwt_token}`;
        }
      } catch (error) {
        console.log(`Error parsing the ${authStorage} from LocalStorage`, error);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
