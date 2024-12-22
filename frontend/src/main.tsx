import './styles/globals.css'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { AppRoutes } from './routes'
import ChatProvider from './context/ChatContext'
import 'highlight.js/styles/github-dark-dimmed.min.css';

const Contexts = () => {
  return (
    <ChatProvider>
      <AppRoutes />
    </ChatProvider>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Contexts />
  </StrictMode>,
)
