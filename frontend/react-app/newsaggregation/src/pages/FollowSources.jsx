"use client"

import { useState, useEffect } from "react"
import axios from "axios"
import {
  FaSpinner,
  FaGlobe,
  FaPlus,
  FaCheck,
  FaRss,
  FaBriefcase,
  FaFilm,
  FaHeartbeat,
  FaFlask,
  FaFutbol,
  FaMicrochip,
  FaNewspaper,
} from "react-icons/fa"
import "./FollowSources.css"

const FollowSources = ({ user }) => {
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [sources, setSources] = useState([])
  const [following, setFollowing] = useState({})
  const [loading, setLoading] = useState(true)
  const [sourcesLoading, setSourcesLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    axios
      .get("/news/categories")
      .then((response) => {
        const fetchedCategories = response.data.categories || response.data || []
        setCategories(fetchedCategories)
        // Auto-select first category if available
        if (fetchedCategories.length > 0 && !selectedCategory) {
          setSelectedCategory(fetchedCategories[0])
        }
      })
      .catch((error) => {
        console.error("Error fetching categories:", error)
        // Fallback to static categories if API fails
        const fallbackCategories = ["business", "entertainment", "health", "science", "sports", "technology"]
        setCategories(fallbackCategories)
        if (!selectedCategory) {
          setSelectedCategory(fallbackCategories[0])
        }
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    if (selectedCategory) {
      setSourcesLoading(true)
      axios
        .get(`/news/websites/${selectedCategory}`)
        .then((response) => {
          setSources(response.data || [])
        })
        .catch((error) => {
          console.error("Error fetching sources:", error)
          setSources([])
        })
        .finally(() => {
          setSourcesLoading(false)
        })
    }
  }, [selectedCategory])

  useEffect(() => {
    if (user) {
      axios
        .get("/user/followed_sources", { headers: { Authorization: `Bearer ${user.token}` } })
        .then((response) => {
          const followedSources = response.data || []
          const followedMap = {}
          followedSources.forEach((source) => {
            followedMap[source.id] = true
          })
          setFollowing(followedMap)
        })
        .catch((error) => console.error("Error fetching followed sources:", error))
    }
  }, [user])

  const toggleFollow = async (source) => {
    if (!user) {
      alert("Please log in to follow sources.")
      return
    }

    const isFollowing = following[source.id]
    const url = isFollowing ? "/user/remove_source" : "/user/add_source"
    const method = isFollowing ? "delete" : "post"

    try {
      // Optimistic update
      setFollowing((prev) => ({ ...prev, [source.id]: !prev[source.id] }))

      await axios({
        method,
        url,
        headers: { Authorization: `Bearer ${user.token}` },
        data: { website_id: source.id },
      })
    } catch (error) {
      console.error("Error updating follow status:", error)
      // Revert on error
      setFollowing((prev) => ({ ...prev, [source.id]: !prev[source.id] }))
      alert(isFollowing ? "Failed to unfollow source" : "Failed to follow source")
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

  const getHostname = (url) => {
    try {
      return new URL(url).hostname
    } catch (error) {
      return url
    }
  }

  if (loading) {
    return (
      <div className="loading-container">
        <FaSpinner className="spinner" />
        <p>Loading categories...</p>
      </div>
    )
  }

  return (
    <div className="follow-sources">
      <h2 className="page-title">Follow News Sources</h2>
      <p className="page-description">
        Customize your news feed by following sources that interest you. Select a category below to browse available
        sources.
      </p>

      <div className="category-container">
        <div className="category-list">
          {categories.map((category) => {
            // Determine icon based on category
            let CategoryIcon
            switch (category) {
              case "business":
                CategoryIcon = FaBriefcase
                break
              case "entertainment":
                CategoryIcon = FaFilm
                break
              case "health":
                CategoryIcon = FaHeartbeat
                break
              case "science":
                CategoryIcon = FaFlask
                break
              case "sports":
                CategoryIcon = FaFutbol
                break
              case "technology":
                CategoryIcon = FaMicrochip
                break
              default:
                CategoryIcon = FaNewspaper
            }

            return (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={selectedCategory === category ? "active" : ""}
              >
                <CategoryIcon className="category-icon" />
                <span>{category.charAt(0).toUpperCase() + category.slice(1)}</span>
              </button>
            )
          })}
        </div>
      </div>

      {selectedCategory && (
        <div className="sources-container">
          <h3 className="sources-title">
            <FaRss className="sources-icon" />
            Sources for {selectedCategory.charAt(0).toUpperCase() + selectedCategory.slice(1)}
          </h3>

          {sourcesLoading ? (
            <div className="loading-container">
              <FaSpinner className="spinner" />
              <p>Loading sources...</p>
            </div>
          ) : sources.length > 0 ? (
            <div className="sources-grid">
              {sources.map((source) => (
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
                    {getHostname(source.url)}
                  </p>
                  <button className={following[source.id] ? "unfollow" : "follow"} onClick={() => toggleFollow(source)}>
                    {following[source.id] ? (
                      <>
                        <FaCheck /> Following
                      </>
                    ) : (
                      <>
                        <FaPlus /> Follow
                      </>
                    )}
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No sources available for this category.</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default FollowSources

