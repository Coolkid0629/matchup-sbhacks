import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Login from './components/Login/Login.jsx'
import Signup from './components/Signup.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Signup />
    <App />
  </StrictMode>,
)
