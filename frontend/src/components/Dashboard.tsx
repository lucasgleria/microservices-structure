import React from 'react'
import { useNavigate } from 'react-router-dom'
import LogoutButton from './LogoutButton'
import styles from '../styles/Dashboard.module.css'

const Dashboard: React.FC = () => {
  const navigate = useNavigate()

  return (
    <div className={styles.container}>
      <div className={styles.formWrapper}>
        <h2 className={styles.title}>Dashboard</h2>
        <button className={styles.button} onClick={() => navigate('/calculator')}>Calculadora</button>
        <button className={styles.button} onClick={() => navigate('/timer')}>Timer</button>
        <LogoutButton />
      </div>
    </div>
  )
}

export default Dashboard
