import React, { useState, useEffect } from 'react'
import axios from 'axios'
import LogoutButton from './LogoutButton'
import { useNavigate } from 'react-router-dom'
import styles from '../styles/Timer.module.css'
import BackButton from './BackButton'

interface TimerStatus {
  running: boolean
  elapsed: number
}

const Timer: React.FC = () => {
  const [status, setStatus] = useState<TimerStatus | null>(null)
  const [error, setError] = useState<string | null>(null)

  const token = localStorage.getItem('token')
  const navigate = useNavigate()

  const fetchStatus = async () => {
    try {
      const response = await axios.get<TimerStatus>('http://localhost:8000/timer/status', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setStatus(response.data)
      setError(null)
    } catch {
      setError('Erro ao buscar status.')
    }
  }

  const sendAction = async (action: string) => {
    try {
      await axios.post(`http://localhost:8000/timer/${action}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      fetchStatus()
    } catch {
      setError(`Erro ao enviar ação: ${action}`)
    }
  }

  useEffect(() => {
    fetchStatus()
    const interval = setInterval(fetchStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h2 className={styles.title}>Timer</h2>
        <button className={styles.button} onClick={() => sendAction('start')}>Start</button>
        <button className={styles.button} onClick={() => sendAction('pause')}>Pause</button>
        <button className={styles.button} onClick={() => sendAction('reset')}>Reset</button>

        {status && (
          <div className={styles.status}>
            <p>Status: {status.running ? 'Rodando' : 'Parado'}</p>
            <p>Tempo decorrido: {status.elapsed} segundos</p>
          </div>
        )}

        {error && <p className={styles.error}>{error}</p>}

      </div>
      <div className={styles.formWrapper1}>
        <BackButton to='/dashboard' />
        <LogoutButton />
      </div>
    </div>
  )
}

export default Timer
