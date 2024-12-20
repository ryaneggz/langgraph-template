import { useNavigate } from 'react-router-dom';
import './ChatLayout.css';

export default function ChatLayout({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();

  return (
    <>
      <button 
        onClick={() => navigate(-1)}
        style={{ 
          border: 'none',
          background: 'none',
          cursor: 'pointer',
          color: 'inherit',
          padding: 0,
          position: 'absolute',
          left: 5,
          top: 5,
        }}
      >
        ← Back
      </button>
      {children}
    </>
  )
}
