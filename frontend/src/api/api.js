import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  'Content-type': 'application/json',
  Accept: 'application/json',
})

export default api