"use client"

import { useState, useEffect } from "react"
import axios from "axios"
import { FaSpinner, FaNewspaper, FaSignInAlt, FaBookmark } from "react-icons/fa"
import { useNavigate } from "react-router-dom"
import NewsCard from "./NewsCard"
import "./NewsFeed.css"

const NewsFeed = ({ page, user }) => {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    let endpoint = "/news/today" // Default to 'today' news
    let headers = {}

    if (page === "ForYou" && user) {
      endpoint = "/user/news"
      headers = { Authorization: `Bearer ${user?.token}` }
    } else if (page === "ReadLater" && user) {
      endpoint = "/user/read_later"
      headers = { Authorization: `Bearer ${user?.token}` }
    }

    setLoading(true)
    setError(null)

    axios
      .get(endpoint, { headers })
      .then((response) => {
        console.log("API Response:", response.data)
        setArticles(response.data || [])
        setError(null)
      })
      .catch((error) => {
        console.error("Error fetching news:", error)
        setError(error.message || "Failed to load articles")
      })
      .finally(() => {
        setLoading(false)
      })
  }, [page, user]) // Re-fetch when `page` or `user` changes

  if (loading) {
    return (
      <div className="loading-container">
        <FaSpinner className="spinner" />
        <p>Loading articles...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-message">
          <p>Error: {error}</p>
          <button onClick={() => window.location.reload()} className="retry-button">
            Try Again
          </button>
        </div>
      </div>
    )
  }

  const getEmptyStateContent = () => {
    if (page === "ForYou" && !user) {
      return {
        icon: <FaSignInAlt className="empty-state-icon" />,
        title: "Personalized Recommendations",
        message: "Sign in to get news tailored to your interests and preferences.",
        buttonText: "Sign In",
        buttonAction: () => alert("Sign in functionality would go here"),
      }
    } else if (page === "ReadLater") {
      return {
        icon: <FaBookmark className="empty-state-icon" />,
        title: "Your Reading List is Empty",
        message: "Save articles to read later by clicking the 'Read Later' button on any article.",
        buttonText: "Browse Articles",
        buttonAction: () => navigate("/today"),
      }
    } else {
      return {
        icon: <FaNewspaper className="empty-state-icon" />,
        title: "No Articles Available",
        message: "We couldn't find any articles matching your criteria. Try again later or adjust your filters.",
        buttonText: "Refresh",
        buttonAction: () => window.location.reload(),
      }
    }
  }

  return (
    <div className="news-feed">
      {articles.length > 0 ? (
        articles.map((article, idx) => (
          <NewsCard
            key={article.id || Math.random().toString(36).substr(2, 9)}
            article={article}
            user={user}
            index={idx}
          />
        ))
      ) : (
        <div className="empty-state">
          {getEmptyStateContent().icon}
          <p>{getEmptyStateContent().title}</p>
          <p className="empty-state-message">{getEmptyStateContent().message}</p>
          <button className="empty-state-button" onClick={getEmptyStateContent().buttonAction}>
            {getEmptyStateContent().buttonText}
          </button>
        </div>
      )}
    </div>
  )
}

export default NewsFeed

