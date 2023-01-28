import axios from "axios";


const BASE_URL = "http://localhost:8000/api"

export const api = axios.create({
  withCredentials: true,
  baseURL: BASE_URL,
  headers: {"Content-Type" : "application/json"}
})

const errorHandler = error => {
  const statusCode = error.response?.status;

  if (statusCode && statusCode !== 401) {
    console.error(error);
  }

  return Promise.reject(error);
}

api.interceptors.response.use(undefined, (error) => {
  return errorHandler(error);
})