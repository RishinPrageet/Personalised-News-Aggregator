"use client"

import { useState, useEffect } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import axios from "axios"
import { FaSpinner, FaSearch, FaCalendarAlt, FaTag, FaArrowLeft } from "react-icons/fa"
import NewsCard from "./NewsCard"
import "./SearchResults.css"

const SearchResults = ({ user }) => {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  // Extract all query parameters from the URL
  const { search } = useLocation()
  const searchParams = new URLSearchParams(search)
  const query = searchParams.get("q") || ""
  const category = searchParams.get("category") || ""
  const fromDate = searchParams.get("from") || ""

  useEffect(() => {
    setLoading(true)
    // Build the query string with all filter parameters
    const params = new URLSearchParams()
    if (query) params.set("q", query)
    if (category) params.set("category", category)
    if (fromDate) params.set("from", fromDate)

    axios
      .get(`/user/search?${params.toString()}`)
      .then((response) => {
        setArticles(response.data || [])
        setError(null)
        setLoading(false)
      })
      .catch((error) => {
        console.error("Error fetching search results:", error)
        setError(error.message)
        setLoading(false)
      })
  }, [query, category, fromDate])

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
      return dateString
    }
  }

  if (loading) {
    return (
      <div className="loading-container">
        <FaSpinner className="spinner" />
        <p>Searching for articles...</p>
      </div>
    )
  }

  if (error) {
    return <div className="error-message">Error: {error}</div>
  }

  return (
    <div className="search-results-container">
      <div className="search-info">
        {query && <h2>Search results for: "{query}"</h2>}
        {!query && <h2>Search Results</h2>}

        {category && (
          <div className="filter-tag">
            <FaTag /> Category: {category.charAt(0).toUpperCase() + category.slice(1)}
          </div>
        )}

        {fromDate && (
          <div className="filter-tag">
            <FaCalendarAlt /> From: {formatDate(fromDate)}
          </div>
        )}
      </div>

      {articles.length > 0 ? (
        <div className="news-feed">
          {articles.map((article, index) => (
            <NewsCard
              key={article.id || Math.random().toString(36).substr(2, 9)}
              article={article}
              user={user}
              index={index}
            />
          ))}
        </div>
      ) : (
        <div className="no-results">
          <FaSearch className="no-results-icon" />
          <h3>No articles found</h3>
          <p>
            We couldn't find any articles matching your search criteria. Try adjusting your search terms or filters.
          </p>
          <button className="search-again-button" onClick={() => navigate(-1)}>
            <FaArrowLeft /> Go Back
          </button>
        </div>
      )}
    </div>
  )
}

export default SearchResults

