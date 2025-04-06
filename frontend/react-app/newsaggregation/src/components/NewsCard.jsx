"use client"

import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"
import { FaSpinner, FaBookmark, FaRegBookmark, FaExternalLinkAlt, FaGlobe, FaClock, FaComments } from "react-icons/fa"
import "./NewsCard.css"

const NewsCard = ({ article, user, index = 0 }) => {
  const [isReadLater, setIsReadLater] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [commentCount, setCommentCount] = useState(0)
  const navigate = useNavigate()

  useEffect(() => {
    if (user) {
      axios
        .get("/user/read_later", {
          headers: { Authorization: `Bearer ${user.token}` },
        })
        .then((response) => {
          const savedArticles = response.data || []
          setIsReadLater(savedArticles.some((item) => item.id === article.id))
        })
        .catch((error) => {
          console.error("Error fetching read later:", error)
          setError("Failed to check saved status")
        })
    }

    // Get comment count from localStorage
    try {
      const comments = JSON.parse(localStorage.getItem(`comments_${article.id}`)) || []
      setCommentCount(comments.length)
    } catch (error) {
      console.error("Error getting comment count:", error)
    }
  }, [user, article.id])

  const toggleReadLater = async (e) => {
    e.stopPropagation() // Prevent card click event

    if (!user) {
      alert("Please log in to save articles.")
      return
    }

    const url = isReadLater ? "/user/remove_read" : "/user/add_read"
    const method = isReadLater ? "delete" : "post"

    try {
      setIsLoading(true)
      setError(null)
      setIsReadLater((prev) => !prev) // Optimistic update for better UX

      await axios({
        method,
        url,
        headers: { Authorization: `Bearer ${user.token}` },
        data: { news_id: article.id },
      })
    } catch (error) {
      console.error("Error updating read later:", error)
      setIsReadLater((prev) => !prev) // Revert state on error
      setError(isReadLater ? "Failed to remove from saved" : "Failed to save article")
    } finally {
      setIsLoading(false)
    }
  }

  // Function to handle read article tracking and navigation
  const handleCardClick = () => {
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

    // Navigate to article detail page
    navigate(`/article/${article.id}`)
  }

  // Format date if available
  const formatDate = (dateString) => {
    if (!dateString) return null

    try {
      const date = new Date(dateString)
      return date.toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
      })
    } catch (e) {
      return null
    }
  }

  const formattedDate = formatDate(article.publishedAt || article.date)

  return (
    <div className="news-card" style={{ "--animation-order": index }} onClick={handleCardClick}>
      <div className="news-card-image-container">
        <img
          src={article.image || article.urlToImage || "https://via.placeholder.com/150?text=No+Image"}
          alt={article.title || "News"}
          onError={(e) => {
            e.target.onerror = null
            e.target.src = "https://via.placeholder.com/150?text=No+Image"
          }}
        />
        {article.category && <div className="article-category">{article.category}</div>}
      </div>

      <div className="news-card-content">
        <h3>{article.title}</h3>
        <div className="article-source">
          <FaGlobe /> {article.source?.name || article.source || "Unknown Source"}
        </div>

        {formattedDate && (
          <div className="article-date">
            <FaClock /> {formattedDate}
          </div>
        )}

        <p>{article.description}</p>

        {error && <div className="error-message">{error}</div>}

        <div className="button-group">
          <button
            onClick={(e) => {
              e.stopPropagation()
              window.open(article.url || article.link, "_blank")
            }}
            aria-label="Read more"
            className="read-more-btn"
          >
            <FaExternalLinkAlt /> Read More
          </button>
          <button
            onClick={toggleReadLater}
            className={`${isReadLater ? "saved" : "read-later"} ${isLoading ? "loading" : ""}`}
            disabled={isLoading}
            aria-label={isReadLater ? "Saved" : "Read Later"}
          >
            {isLoading ? <FaSpinner className="spinner" /> : isReadLater ? <FaBookmark /> : <FaRegBookmark />}
            {isReadLater ? "Saved" : "Read Later"}
          </button>
        </div>

        {commentCount > 0 && (
          <div className="comment-count">
            <FaComments /> {commentCount} comment{commentCount !== 1 ? "s" : ""}
          </div>
        )}
      </div>
    </div>
  )
}

export default NewsCard

