"use client"

import { useState, useEffect } from "react"
import { useNavigate, useLocation } from "react-router-dom"
import { FaSearch, FaFilter, FaSun, FaMoon, FaNewspaper, FaSignOutAlt, FaUser } from "react-icons/fa"
import axios from "axios"
import { useTheme } from "../context/ThemeContext"
import "./Header.css"

const Header = ({ user }) => {
  const navigate = useNavigate()
  const location = useLocation()
  const searchParams = new URLSearchParams(location.search)
  const { theme, toggleTheme } = useTheme()

  // Initialize state from URL parameters if they exist
  const [searchQuery, setSearchQuery] = useState(searchParams.get("q") || "")
  const [showFilters, setShowFilters] = useState(false)
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [category, setCategory] = useState(searchParams.get("category") || "")
  const [date, setDate] = useState(searchParams.get("from") || "")
  const [categories, setCategories] = useState([])
  const [activeFilters, setActiveFilters] = useState(false)
  const [loading, setLoading] = useState(false)
  const [loggingOut, setLoggingOut] = useState(false)

  useEffect(() => {
    // Fetch categories from API
    setLoading(true)
    axios
      .get("/news/categories")
      .then((response) => {
        const fetchedCategories = response.data.categories || response.data || []
        setCategories(fetchedCategories)
      })
      .catch((error) => {
        console.error("Error fetching categories:", error)
        // Fallback to static categories if API fails
        setCategories(["business", "entertainment", "health", "science", "sports", "technology"])
      })
      .finally(() => {
        setLoading(false)
      })

    // Check if any filters are active
    setActiveFilters(!!(category || date))
  }, [category, date])

  const handleSearch = () => {
    const params = new URLSearchParams()
    if (searchQuery.trim()) params.set("q", searchQuery.trim())
    if (category) params.set("category", category)
    if (date) params.set("from", date)

    navigate(`/search?${params.toString()}`)
    setShowFilters(false) // Hide filters after applying
  }

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSearch()
    }
  }

  const clearFilters = () => {
    setCategory("")
    setDate("")
    setActiveFilters(false)

    // If we're already on the search page, update the URL
    if (location.pathname === "/search") {
      const params = new URLSearchParams()
      if (searchQuery.trim()) params.set("q", searchQuery.trim())
      navigate(`/search?${params.toString()}`)
    }
  }

  const selectCategory = (cat) => {
    setCategory(cat === category ? "" : cat)
  }

  const handleLogout = async () => {
    try {
      setLoggingOut(true)
      await axios.get("/user/logout")
      // Clear any local user data and redirect to home
      navigate("/")
      window.location.reload() // Force a reload to clear all state
    } catch (error) {
      console.error("Logout failed:", error)
      alert("Failed to log out. Please try again.")
    } finally {
      setLoggingOut(false)
      setShowUserMenu(false)
    }
  }

  return (
    <header className="header">
      <div className="header-left">
        <h1 className="logo">
          <FaNewspaper className="logo-icon" />
          News Aggregator
        </h1>
      </div>

      {/* Filter & Search Section */}
      <div className="search-container">
        {/* Filter Button with active indicator */}
        <button
          className={`filter-btn ${activeFilters ? "filter-active" : ""}`}
          onClick={() => setShowFilters(!showFilters)}
          aria-label="Filter"
        >
          <FaFilter />
          {activeFilters && <span className="filter-indicator"></span>}
        </button>

        {/* Filter Dropdown */}
        {showFilters && (
          <div className="filter-dropdown">
            <div className="filter-header">
              <h4>Filter Articles</h4>
              {activeFilters && (
                <button onClick={clearFilters} className="clear-filters-btn">
                  Clear All
                </button>
              )}
            </div>

            <div className="filter-group">
              <label htmlFor="category-select">Category</label>
              {loading ? (
                <p>Loading categories...</p>
              ) : (
                <div className="category-chips">
                  {categories.map((cat) => (
                    <span
                      key={cat}
                      className={`category-chip ${category === cat ? "selected" : ""}`}
                      onClick={() => selectCategory(cat)}
                    >
                      {cat.charAt(0).toUpperCase() + cat.slice(1)}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="filter-group">
              <label htmlFor="date-select">From Date</label>
              <input id="date-select" type="date" value={date} onChange={(e) => setDate(e.target.value)} />
            </div>

            <button onClick={handleSearch} className="apply-filters-btn">
              Apply Filters
            </button>
          </div>
        )}

        {/* Search Input */}
        <input
          type="text"
          placeholder="Search news..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={handleKeyPress}
          className="search-input"
        />
        <button onClick={handleSearch} className="search-btn" aria-label="Search">
          <FaSearch />
        </button>
      </div>

      <div className="header-right">
        {/* Theme Toggle Button */}
        <button
          className="theme-toggle-btn"
          onClick={toggleTheme}
          aria-label={theme === "light" ? "Switch to dark mode" : "Switch to light mode"}
        >
          {theme === "light" ? <FaMoon /> : <FaSun />}
        </button>

        {/* User Menu */}
        {user ? (
          <div className="user-menu-container">
            <button className="user-menu-button" onClick={() => setShowUserMenu(!showUserMenu)} aria-label="User menu">
              <div className="user-avatar">{user.username ? user.username.charAt(0).toUpperCase() : "U"}</div>
            </button>

            {showUserMenu && (
              <div className="user-dropdown">
                <div className="user-dropdown-header">
                  <div className="user-dropdown-name">{user.username}</div>
                  <div className="user-dropdown-email">{user.email || "user@example.com"}</div>
                </div>

                <div className="user-dropdown-options">
                  <button className="user-dropdown-option">
                    <FaUser />
                    Profile
                  </button>

                  <button className="user-dropdown-option" onClick={handleLogout} disabled={loggingOut}>
                    <FaSignOutAlt />
                    {loggingOut ? "Logging out..." : "Logout"}
                  </button>
                </div>
              </div>
            )}
          </div>
        ) : (
          <button className="login-button" onClick={() => alert("Sign in functionality would go here")}>
            Sign In
          </button>
        )}
      </div>
    </header>
  )
}

export default Header

