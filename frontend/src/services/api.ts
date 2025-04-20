import axios, { AxiosInstance } from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const api: AxiosInstance = axios.create({
    baseURL: API_BASE_URL,
});

interface UserData {
    email: string;
    password: string;
    name?: string;
    [key: string]: any;
}

export const loginUser = async (email: string, password: string): Promise<any> => {
    const response = await api.post("/auth/login", {
        username: email,
        password,
    });
    return response.data;
};

export const registerUser = async (userData: UserData): Promise<any> => {
    const response = await api.post("/users/register", userData);
    return response.data;
};

export default api;