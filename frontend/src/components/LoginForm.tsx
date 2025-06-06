import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import styles from '../styles/LoginForm.module.css'

interface LoginResponse {
  access_token: string
  token_type: string
}

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  const { setToken } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await axios.post<LoginResponse>('http://localhost:8000/auth/login', {
        email,
        password,
      })

      if (response.data && response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        setToken(response.data.access_token)
        setError(null)
        navigate('/dashboard')
      } else {
        throw new Error('Token inválido.')
      }

    } catch (err: any) {
      console.error("Erro de autenticação:", err.response?.status || err.message)
      setError('Login failed. Check credentials.')

      localStorage.removeItem('token')
      setToken(null)
    }
  }



  return (
    <div className={styles.container}>
      <div className={styles.formWrapper}>
        <h2 className={styles.title}>Login</h2>
        <form onSubmit={handleSubmit}>
          <div className={styles.formGroup}>
            <label className={styles.label}>Email:</label>
            <input
              className={styles.input}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label className={styles.label}>Password:</label>
            <input
              className={styles.input}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button className={styles.button} type="submit">Login</button>
        </form>

        {error && <p className={styles.error}>{error}</p>}
      </div>
    </div>
  )
}

export default LoginForm
