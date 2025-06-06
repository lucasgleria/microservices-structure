import React from 'react'
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom'
import LoginForm from './components/LoginForm'
import Dashboard from './components/Dashboard'
import Calculator from './components/Calculator'
import Timer from './components/Timer'
import PrivateRoute from './components/PrivateRoute'
import { AuthProvider } from './context/AuthContext'

function App() {
  return (
    <Router>
      <AuthProvider>
          <Routes>
            <Route path="/" element={<LoginForm />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/calculator" element={
              <PrivateRoute>
                <Calculator />
              </PrivateRoute>
            } />
            <Route path="/timer" element={
              <PrivateRoute>
                <Timer />
              </PrivateRoute>
            } />
          </Routes>
      </AuthProvider>
    </Router>
  )
}

export default App
