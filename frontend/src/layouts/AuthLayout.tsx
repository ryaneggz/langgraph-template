export default function NoAuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <header>
        <h1>Thread Agents</h1>
      </header>
      {children}
      <footer>
        <p>&copy; 2024 Your Company</p>
      </footer>
    </>
  )
}
