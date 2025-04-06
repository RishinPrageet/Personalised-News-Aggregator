"use client"

import { useState, useEffect } from "react"
import { FaSpinner, FaBookOpen, FaExternalLinkAlt, FaGlobe, FaClock, FaNewspaper } from "react-icons/fa"
import { useNavigate } from "react-router-dom"
import "./ReadArticles.css"

const ReadArticles = () => {
  const [readArticles, setReadArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    // Simulate loading for better UX
    setTimeout(() => {
      try {
        const storedArticles = JSON.parse(localStorage.getItem("readArticles")) || []
        setReadArticles(storedArticles)
      } catch (error) {
        console.error("Error parsing stored articles:", error)
        setReadArticles([])
      } finally {
        setLoading(false)
      }
    }, 500)
  }, [])

  // Format date if available
  const formatDate = (dateString) => {
    if (!dateString) return "Unknown date"

    try {
      const date = new Date(dateString)
      return date.toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
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
        <p>Loading your read articles...</p>
      </div>
    )
  }

  return (
    <div className="read-articles-container">
      <h1 className="page-title">Read Articles</h1>
      <p className="page-description">
        Keep track of articles you've read. This helps you maintain a reading history and easily revisit important
        content.
      </p>

      {readArticles.length === 0 ? (
        <div className="empty-state">
          <FaBookOpen className="empty-state-icon" />
          <p>No articles read yet</p>
          <p className="empty-state-message">
            Articles you read will appear here for easy reference. Start exploring to build your reading history.
          </p>
          <button className="empty-state-button" onClick={() => navigate("/today")}>
            <FaNewspaper /> Browse Articles
          </button>
        </div>
      ) : (
        <div className="articles-grid">
          {readArticles.map((article, index) => (
            <div key={index} className="article-card">
              <img
                src={article.urlToImage || article.image || "https://via.placeholder.com/150?text=No+Image"}
                alt={article.title || "News"}
                className="article-image"
                onError={(e) => {
                  e.target.onerror = null
                  e.target.src = "https://via.placeholder.com/150?text=No+Image"
                }}
              />
              <div className="article-content">
                <h3>{article.title}</h3>
                <div className="article-source">
                  <FaGlobe /> {article.source?.name || article.source || "Unknown Source"}
                </div>
                <div className="article-date">
                  <FaClock /> {formatDate(article.publishedAt || article.date)}
                </div>
                <a
                  href={article.url || article.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="view-article"
                >
                  <FaExternalLinkAlt /> View Article
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ReadArticles

