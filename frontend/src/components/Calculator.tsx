import React, { useState } from 'react'
import axios from 'axios'
import LogoutButton from './LogoutButton'
import { useNavigate } from 'react-router-dom'
import styles from '../styles/Calculator.module.css'
import BackButton from './BackButton'

interface CalculationResponse {
  result: number
}

const Calculator: React.FC = () => {
  const [a, setA] = useState<number>(0)
  const [b, setB] = useState<number>(0)
  const [operation, setOperation] = useState<string>('+')
  const [result, setResult] = useState<number | null>(null)
  const [error, setError] = useState<string | null>(null)

  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const token = localStorage.getItem('token')
      const response = await axios.post<CalculationResponse>('http://localhost:8000/calculate',
        { a, b, operation },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setResult(response.data.result)
      setError(null)
    } catch {
      setError('Erro na operação.')
      setResult(null)
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.formWrapper}>
        <h2 className={styles.title}>Calculadora</h2>
        <form onSubmit={handleSubmit}>
          <div className={styles.formGroup}>
            <label className={styles.label}>A:</label>
            <input
              className={styles.input}
              type="number"
              value={a}
              onChange={(e) => setA(Number(e.target.value))}
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label className={styles.label}>B:</label>
            <input
              className={styles.input}
              type="number"
              value={b}
              onChange={(e) => setB(Number(e.target.value))}
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label className={styles.label}>Operação:</label>
            <select
              className={styles.select}
              value={operation}
              onChange={(e) => setOperation(e.target.value)}
            >
              <option value="+">Soma</option>
              <option value="-">Subtração</option>
              <option value="*">Multiplicação</option>
              <option value="/">Divisão</option>
            </select>
          </div>

          <button className={styles.button} type="submit">Calcular</button>
        </form>

        {result !== null && <p className={styles.result}>Resultado: {result}</p>}
        {error && <p className={styles.error}>{error}</p>}

      </div>
      <div className={styles.formWrapper1}>
        <BackButton to='/dashboard' />
        <LogoutButton />
      </div>
    </div>
  )
}

export default Calculator
