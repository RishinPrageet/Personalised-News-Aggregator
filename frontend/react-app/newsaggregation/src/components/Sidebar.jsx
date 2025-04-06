"use client"

import { useState, useEffect } from "react"
import { Link, useLocation, useNavigate } from "react-router-dom"
import axios from "axios"
import {
  FaHome,
  FaUserAlt,
  FaNewspaper,
  FaRss,
  FaBookmark,
  FaBookOpen,
  FaUsers,
  FaChartBar,
  FaBars,
  FaTimes,
  FaSignOutAlt,
} from "react-icons/fa"
import { useTheme } from "../context/ThemeContext"
import "./Sidebar.css"

// Update the Sidebar component to accept props for controlling state
const Sidebar = ({ user, isOpen, onToggle }) => {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 1024)
  const [loggingOut, setLoggingOut] = useState(false)
  const location = useLocation()
  const navigate = useNavigate()
  const { theme } = useTheme()

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 1024)
    }

    window.addEventListener("resize", handleResize)
    return () => window.removeEventListener("resize", handleResize)
  }, [])

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
    }
  }

  // Define navigation items
  const navItems = [
    { path: "/home", icon: <FaHome />, label: "Home" },
    { path: "/ForYou", icon: <FaUserAlt />, label: "For You" },
    { path: "/today", icon: <FaNewspaper />, label: "Today" },
    { path: "/follow-sources", icon: <FaRss />, label: "Follow Sources" },
    { path: "/read-later", icon: <FaBookmark />, label: "Read Later" },
    { path: "/unread", icon: <FaBookOpen />, label: "Read Articles" },
    { path: "/following", icon: <FaUsers />, label: "Following" },
    { path: "/analytics", icon: <FaChartBar />, label: "Analytics" },
  ]

  return (
    <>
      <div className={`sidebar-toggle ${isOpen ? "open" : "closed"}`} onClick={onToggle}>
        {isOpen ? <FaTimes /> : <FaBars />}
      </div>

      <aside className={`sidebar ${isOpen ? "open" : "closed"} ${theme === "dark" ? "dark" : ""}`}>
        <div className="sidebar-header">
          <h2 className="sidebar-title">
            <FaNewspaper className="sidebar-logo" />
            <span className="sidebar-title-text">NewsAgg</span>
          </h2>
        </div>

        <nav className="sidebar-nav">
          <ul>
            {navItems.map((item) => (
              <li key={item.path}>
                <Link to={item.path} className={location.pathname === item.path ? "active" : ""}>
                  <span className="sidebar-icon">{item.icon}</span>
                  <span className="sidebar-label">{item.label}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <div className="sidebar-footer">
          {user ? (
            <>
              <div className="user-info">
                <div className="user-avatar">{user.username ? user.username.charAt(0).toUpperCase() : "U"}</div>
                <div className="user-details">
                  <p className="username">{user.username}</p>
                  <p className="user-email">{user.email || "user@example.com"}</p>
                </div>
              </div>
              <button className="logout-button" onClick={handleLogout} disabled={loggingOut}>
                <FaSignOutAlt />
                <span>{loggingOut ? "Logging out..." : "Logout"}</span>
              </button>
            </>
          ) : (
            <div className="login-prompt">
              <p>Sign in to personalize your news feed</p>
              <button className="login-button" onClick={() => alert("Sign in functionality would go here")}>
                Sign In
              </button>
            </div>
          )}
        </div>
      </aside>

      {/* Overlay for mobile */}
      {isMobile && isOpen && <div className="sidebar-overlay" onClick={onToggle}></div>}
    </>
  )
}

export default Sidebar

