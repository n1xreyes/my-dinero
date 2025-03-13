import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const api = axios.create({
    baseURL: API_BASE_URL,
});

export const loginUser = async (email, password) => {
    const response = await api.post("/auth/login", {
        username: email,
        password,
    });
    return response.data;
};

export const registerUser = async (userData) => {
    const response = await api.post("/users/register", userData);
    return response.data;
};

export default api;
