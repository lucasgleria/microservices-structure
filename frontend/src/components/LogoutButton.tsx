import React from 'react'
import { useAuth } from '../context/AuthContext'
import styles from '../styles/LogoutButton.module.css'

const LogoutButton: React.FC = () => {
  const { logout } = useAuth()

  return <button className={styles.button} onClick={logout}>Logout</button>
}

export default LogoutButton
