import './styles/globals.css'
import 'highlight.js/styles/github-dark-dimmed.min.css';
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { AppRoutes } from './routes'
import ChatProvider from './context/ChatContext'
import ThemeProvider from './context/ThemeContext'

const Contexts = () => {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <ChatProvider>
        <AppRoutes />
      </ChatProvider>
    </ThemeProvider>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Contexts />
  </StrictMode>,
)
