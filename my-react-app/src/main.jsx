import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Login from './components/Login/Login.jsx'
import Signup from './components/Signup.jsx'
import Navbar from './components/Navbar/NavbarComponent.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Navbar />
  </StrictMode>,
)
