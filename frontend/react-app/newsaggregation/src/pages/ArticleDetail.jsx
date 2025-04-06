"use client"

import { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import axios from "axios"
import {
  FaArrowLeft,
  FaBookmark,
  FaRegBookmark,
  FaShare,
  FaGlobe,
  FaClock,
  FaSpinner,
  FaUser,
  FaPaperPlane,
  FaExclamationTriangle,
} from "react-icons/fa"
import "./ArticleDetail.css"

const ArticleDetail = ({ user }) => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [article, setArticle] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [isReadLater, setIsReadLater] = useState(false)
  const [comments, setComments] = useState([])
  const [newComment, setNewComment] = useState("")
  const [submittingComment, setSubmittingComment] = useState(false)

  // Fetch article data
  useEffect(() => {
    const fetchArticle = async () => {
      try {
        setLoading(true)
        const response = await axios.get(`/news/${id}`)
        setArticle(response.data)
        console.log(article)
      } catch (error) {
        console.error("Error fetching article:", error)
        setError("Failed to load article. Please try again later.")
      } finally {
        setLoading(false)
      }
    }

    fetchArticle()
  }, [id])

  // This will update the read article in localStorage when viewing an article
  useEffect(() => {
    if (article) {
      // Store the read article in localStorage
      try {
        const readArticles = JSON.parse(localStorage.getItem("readArticles")) || []

        // Check if article is already in the list
        if (!readArticles.some((item) => item.id === article.id)) {
          readArticles.push(article)
          localStorage.setItem("readArticles", JSON.stringify(readArticles))
        }
      } catch (error) {
        console.error("Error saving read article:", error)
      }
    }
  }, [article])

  // Fetch comments
  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await axios.get(`/news/${id}/comments`)
        setComments(response.data)
      } catch (error) {
        console.error("Error fetching comments:", error)
      }
    }

    fetchComments()
  }, [id])

  const toggleReadLater = async () => {
    if (!user) {
      alert("Please log in to save articles.")
      return
    }

    const url = isReadLater ? "/user/remove_read" : "/user/add_read"
    const method = isReadLater ? "delete" : "post"

    try {
      setIsReadLater((prev) => !prev) // Optimistic update

      await axios({
        method,
        url,
        headers: { Authorization: `Bearer ${user.token}` },
        data: { news_id: article.id },
      })
    } catch (error) {
      console.error("Error updating read later:", error)
      setIsReadLater((prev) => !prev) // Revert on error
      alert(isReadLater ? "Failed to remove from saved" : "Failed to save article")
    }
  }

  const handleSubmitComment = async (e) => {
    e.preventDefault()

    if (!newComment.trim()) return

    if (!user) {
      alert("Please log in to comment.")
      return
    }

    try {
      setSubmittingComment(true)
      const response = await axios.post(
        `/news/${id}/comments`,
        { text: newComment },
        { headers: { Authorization: `Bearer ${user.token}` } },
      )
      setComments((prev) => [...prev, response.data])
      setNewComment("")
    } catch (error) {
      console.error("Error posting comment:", error)
      alert("Failed to post comment. Please try again.")
    } finally {
      setSubmittingComment(false)
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return "Unknown date"

    try {
      const date = new Date(dateString)
      return date.toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric",
      })
    } catch (e) {
      return "Unknown date"
    }
  }

  if (loading) {
    return (
      <div className="loading-container">
        <FaSpinner className="spinner" />
        <p>Loading article...</p>
      </div>
    )
  }

  if (error || !article) {
    return (
      <div className="error-container">
        <div className="error-message">
          <FaExclamationTriangle className="error-icon" />
          <h3>Error Loading Article</h3>
          <p>{error || "Article not found"}</p>
          <button onClick={() => navigate(-1)} className="back-button">
            <FaArrowLeft /> Go Back
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="article-detail-container">
      <div className="article-detail-content">
        <button onClick={() => navigate(-1)} className="back-button">
          <FaArrowLeft /> Back
        </button>

        <div className="article-header">
          <h1>{article.title}</h1>

          <div className="article-meta">
            <div className="article-source">
              <FaGlobe /> {article.website?.name || "Unknown Source"}
            </div>
            <div className="article-date">
              <FaClock /> {formatDate(article.published)}
            </div>
          </div>

          <div className="article-actions">
            <button className={`save-button ${isReadLater ? "saved" : ""}`} onClick={toggleReadLater}>
              {isReadLater ? <FaBookmark /> : <FaRegBookmark />}
              {isReadLater ? "Saved" : "Save"}
            </button>
            <button className="share-button">
              <FaShare /> Share
            </button>
          </div>
        </div>

        {article.image && (
          <div className="article-image-container">
            <img
              src={article.image || "/placeholder.svg"}
              alt={article.title}
              className="article-image"
              onError={(e) => {
                e.target.onerror = null
                e.target.src = "https://via.placeholder.com/800x400?text=No+Image"
              }}
            />
          </div>
        )}

        <div className="article-summary">
          <h2>Summary</h2>
          <p>{article.description}</p>
        </div>

        <div className="article-comments">
          <h2>Comments ({comments.length})</h2>

          <form onSubmit={handleSubmitComment} className="comment-form">
            <div className="comment-input-container">
              <div className="comment-avatar">{user ? user.username.charAt(0).toUpperCase() : <FaUser />}</div>
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder={user ? "Add a comment..." : "Please sign in to comment"}
                disabled={!user || submittingComment}
                className="comment-input"
              />
            </div>
            <div className="comment-form-actions">
              <button
                type="submit"
                className="submit-comment-button"
                disabled={!user || !newComment.trim() || submittingComment}
              >
                {submittingComment ? <FaSpinner className="spinner" /> : <FaPaperPlane />}
                Post Comment
              </button>
            </div>
          </form>

          <div className="comments-list">
            {comments.length > 0 ? (
              comments.map((comment) => (
                <div key={comment.id} className="comment">
                  <div className="comment-avatar">{comment.user_id}</div>
                  <div className="comment-content">
                    <p className="comment-text">{comment.comment}</p>
                  </div>
                </div>
              ))
            ) : (
              <div className="no-comments">
                <p>No comments yet. Be the first to share your thoughts!</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ArticleDetail

