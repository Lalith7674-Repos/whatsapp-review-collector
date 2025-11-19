// App.jsx - Main React component
import React, { useEffect, useState } from 'react'
import ReviewsTable from './components/ReviewsTable'

function App() {
  const [reviews, setReviews] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchReviews()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const fetchReviews = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await fetch('/api/reviews')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setReviews(data)
    } catch (err) {
      console.error('Error fetching reviews:', err)
      setError(err.message || 'Failed to fetch reviews')
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString)
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short'
      })
    } catch (e) {
      return dateString
    }
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>WhatsApp Product Reviews</h1>
        <button onClick={fetchReviews} disabled={loading} className="refresh-btn">
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </header>

      {error && (
        <div className="error-message">
          <p>Error: {error}</p>
          <button onClick={fetchReviews}>Retry</button>
        </div>
      )}

      {loading && reviews.length === 0 ? (
        <div className="loading-message">Loading reviews...</div>
      ) : reviews.length === 0 ? (
        <div className="empty-message">No reviews yet. Send a WhatsApp message to get started!</div>
      ) : (
        <ReviewsTable reviews={reviews} formatDate={formatDate} />
      )}
    </div>
  )
}

export default App
