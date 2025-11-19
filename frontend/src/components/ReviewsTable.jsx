// ReviewsTable.jsx - Reusable table component
import React from 'react'

function ReviewsTable({ reviews, formatDate }) {
  // Default formatDate function if not provided
  const defaultFormatDate = (dateString) => {
    try {
      if (!dateString) return 'N/A'
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
      return dateString || 'N/A'
    }
  }

  const formatDateSafe = formatDate || defaultFormatDate

  if (!reviews || reviews.length === 0) {
    return <div className="empty-message">No reviews to display</div>
  }

  return (
    <div className="table-container">
      <table className="reviews-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Contact Number</th>
            <th>User Name</th>
            <th>Product Name</th>
            <th>Review</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {reviews.map((review) => (
            <tr key={review.id}>
              <td>{review.id || 'N/A'}</td>
              <td>{review.contact_number || 'N/A'}</td>
              <td>{review.user_name || 'N/A'}</td>
              <td>{review.product_name || 'N/A'}</td>
              <td className="review-text">{review.product_review || 'N/A'}</td>
              <td>{formatDateSafe(review.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="table-footer">
        <p>Total reviews: {reviews.length}</p>
      </div>
    </div>
  )
}

export default ReviewsTable
