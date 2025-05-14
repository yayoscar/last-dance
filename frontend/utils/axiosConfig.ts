import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://localhost:3200/api/v1/", // Cambia esto según tu backend
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptores para manejar errores globales
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("Error en la respuesta Axios:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default axiosInstance;
