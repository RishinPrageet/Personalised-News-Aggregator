"use client"

import { useEffect, useState } from "react"
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import axios from "axios"
import { FaSpinner } from "react-icons/fa"
import Header from "./components/Header"
import Sidebar from "./components/Sidebar"
import HomePage from "./pages/HomePage"
import Today from "./pages/Today"
import ForYou from "./pages/ForYou"
import FollowSources from "./pages/FollowSources"
import ReadLater from "./pages/ReadLater"
import UnreadArticles from "./pages/ReadArticles"
import Following from "./pages/Following"
import Analytics from "./pages/Analytics"
import SearchResults from "./components/SearchResults"
import ArticleDetail from "./pages/ArticleDetail"
import Chatbot from "./components/Chatbot"
import "./App.css"

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  useEffect(() => {
    axios
      .get("/user/me", { withCredentials: true }) // Ensure cookies (JWT) are sent
      .then((response) => {
        setUser(response.data) // Expecting { id, username }
      })
      .catch((error) => {
        console.error("Error fetching user data:", error)
        setUser(null) // Reset on error
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  const handleSidebarToggle = () => {
    setSidebarOpen(!sidebarOpen)
  }

  if (loading) {
    return (
      <div className="app-loading">
        <FaSpinner className="spinner" />
        <p>Loading application...</p>
      </div>
    )
  }

  return (
    <Router>
      <div className="app-container">
        <Sidebar user={user} isOpen={sidebarOpen} onToggle={handleSidebarToggle} />
        <div className={`app-main ${sidebarOpen ? "sidebar-open" : "sidebar-closed"}`}>
          <Header user={user} /> {/* Pass user data to Header */}
          <div className="app-content">
            <Routes>
              <Route path="/user/profile" element={<Navigate to="/home" replace />} />
              <Route path="/home" element={<HomePage user={user} />} />
              <Route path="/ForYou" element={<ForYou user={user} />} />
              <Route path="/today" element={<Today user={user} />} />
              <Route path="/follow-sources" element={<FollowSources user={user} />} />
              <Route path="/read-later" element={<ReadLater user={user} />} />
              <Route path="/unread" element={<UnreadArticles />} />
              <Route path="/following" element={<Following user={user} />} />
              <Route path="/analytics" element={<Analytics user={user} />} />
              <Route path="/search" element={<SearchResults user={user} />} />
              <Route path="/article/:id" element={<ArticleDetail user={user} />} />
              <Route path="/" element={<Navigate to="/home" replace />} />
            </Routes>
          </div>
          <Chatbot />
        </div>
      </div>
    </Router>
  )
}

export default App

