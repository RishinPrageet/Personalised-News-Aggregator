"use client"

import { useState, useEffect } from "react"
import axios from "axios"
import { FaUserMinus, FaRss, FaGlobe, FaPlus, FaSpinner } from "react-icons/fa"
import { useNavigate } from "react-router-dom"
import "./Following.css"

const Following = ({ user }) => {
  const [followedSources, setFollowedSources] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    if (user) {
      setLoading(true)
      axios
        .get("/user/followed_sources", { headers: { Authorization: `Bearer ${user.token}` } })
        .then((response) => {
          setFollowedSources(response.data || [])
        })
        .catch((error) => console.error("Error fetching followed sources:", error))
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [user])

  const unfollowSource = async (sourceId) => {
    try {
      await axios.delete("/user/remove_source", {
        headers: { Authorization: `Bearer ${user.token}` },
        data: { website_id: sourceId },
      })

      setFollowedSources((prev) => prev.filter((source) => source.id !== sourceId))
    } catch (error) {
      console.error("Error unfollowing source:", error)
    }
  }

  const getLogoUrl = (sourceUrl) => {
    try {
      const hostname = new URL(sourceUrl).hostname
      return `https://logo.clearbit.com/${hostname}`
    } catch (error) {
      return ""
    }
  }

  if (loading) {
    return (
      <div className="loading-container">
        <FaSpinner className="spinner" />
        <p>Loading your followed sources...</p>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="following-container">
        <h2 className="page-title">Followed Sources</h2>
        <p className="page-description">
          Follow your favorite news sources to customize your news feed and stay updated with content that matters to
          you.
        </p>

        <div className="empty-state">
          <FaRss className="empty-state-icon" />
          <p>Sign in to follow sources</p>
          <p className="empty-state-message">
            You need to be signed in to follow sources and customize your news feed.
          </p>
          <button className="empty-state-button" onClick={() => alert("Sign in functionality would go here")}>
            Sign In
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="following-container">
      <h2 className="page-title">Followed Sources</h2>
      <p className="page-description">
        Manage the news sources you follow. These sources will appear in your personalized feed to keep you informed.
      </p>

      {followedSources.length > 0 ? (
        <div className="sources-grid">
          {followedSources.map((source) => (
            <div key={source.id} className="source-card">
              <img
                src={getLogoUrl(source.url) || "/placeholder.svg"}
                alt={source.name}
                className="source-logo"
                onError={(e) => {
                  e.target.onerror = null
                  e.target.src = "https://via.placeholder.com/80?text=Logo"
                }}
              />
              <h4>{source.name}</h4>
              <p className="source-url">
                <FaGlobe style={{ marginRight: "6px", fontSize: "12px" }} />
                {new URL(source.url).hostname}
              </p>
              <button className="unfollow" onClick={() => unfollowSource(source.id)}>
                <FaUserMinus /> Unfollow
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <FaRss className="empty-state-icon" />
          <p>You are not following any sources</p>
          <p className="empty-state-message">
            Follow news sources to customize your feed and stay updated with content that matters to you.
          </p>
          <button className="empty-state-button" onClick={() => navigate("/follow-sources")}>
            <FaPlus /> Follow Sources
          </button>
        </div>
      )}
    </div>
  )
}

export default Following

