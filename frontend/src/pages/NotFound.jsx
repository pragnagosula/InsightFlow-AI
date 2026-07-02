import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="min-h-screen bg-surface-900 flex items-center justify-center">
      <div className="text-center">
        <p className="text-6xl font-bold text-surface-600 mb-4">404</p>
        <h1 className="text-text-primary font-semibold text-lg mb-2">Page not found</h1>
        <p className="text-text-muted text-sm mb-6">The page you're looking for doesn't exist.</p>
        <Link to="/" className="btn-primary inline-block">Back to Home</Link>
      </div>
    </div>
  )
}
