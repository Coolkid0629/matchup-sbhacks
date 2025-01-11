import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Login from './components/Login/Login.jsx'
import Signup from './components/Signup.jsx'
import NavbarComponent from './components/NavbarComponent.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <NavbarComponent />
  </StrictMode>,
) 