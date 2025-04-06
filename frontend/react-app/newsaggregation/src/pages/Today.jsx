"use client"

import { useRef } from "react"
import NewsFeed from "../components/NewsFeed"
import "./Today.css"

const Today = ({ user }) => {
  // Create a ref for the NewsFeed container to get its dimensions
  const containerRef = useRef(null)

  return (
    <div className="today-container">
      <h2 className="today-title">Today's News</h2>
      <p className="page-description">
        Stay informed with the latest headlines and breaking news from around the world, curated for you and updated
        throughout the day.
      </p>
      <div className="news-grid" ref={containerRef}>
        <NewsFeed page="today" user={user} />
      </div>
    </div>
  )
}

export default Today

