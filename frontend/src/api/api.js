import axios from 'axios'

const API_URL = import.meta.env.BACKEND_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: 'http://localhost:8000',
  'Content-type': 'application/json',
  Accept: 'application/json',
})

export default api