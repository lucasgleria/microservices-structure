import React from 'react'
import { useNavigate } from 'react-router-dom'
import styles from '../styles/BackButton.module.css'  // Reutiliza .button

interface BackButtonProps {
  to: string
}

const BackButton: React.FC<BackButtonProps> = ({ to }) => {
  const navigate = useNavigate()

  return (
    <button className={styles.button} onClick={() => navigate(to)}>
      Voltar
    </button>
  )
}

export default BackButton
