"use client"

import { useState, useEffect } from "react"
import { FaChartBar, FaBookOpen, FaRegClock, FaNewspaper, FaHashtag, FaEye, FaBookmark } from "react-icons/fa"
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"
import "./Analytics.css"

const Analytics = ({ user }) => {
  const [timeframe, setTimeframe] = useState("week")
  const [readArticles, setReadArticles] = useState([])
  const [savedArticles, setSavedArticles] = useState([])
  const [totalArticlesRead, setTotalArticlesRead] = useState(0)
  const [totalArticlesSaved, setTotalArticlesSaved] = useState(0)

  useEffect(() => {
    // Load read articles from localStorage
    try {
      const storedArticles = JSON.parse(localStorage.getItem("readArticles")) || []
      setReadArticles(storedArticles)
      setTotalArticlesRead(storedArticles.length)
    } catch (error) {
      console.error("Error parsing stored read articles:", error)
    }

    // Simulate saved articles data
    // In a real app, this would come from your API
    try {
      // For demo purposes, use half of read articles as saved
      const storedArticles = JSON.parse(localStorage.getItem("readArticles")) || []
      const demoSavedArticles = storedArticles.slice(0, Math.floor(storedArticles.length / 2))
      setSavedArticles(demoSavedArticles)
      setTotalArticlesSaved(demoSavedArticles.length)
    } catch (error) {
      console.error("Error setting saved articles:", error)
    }
  }, [])

  // Generate reading activity data based on timestamps of read articles
  const getReadingActivityData = () => {
    // Get date labels based on timeframe
    const labels = []
    const now = new Date()
    const counts = {}

    if (timeframe === "week") {
      for (let i = 6; i >= 0; i--) {
        const date = new Date(now)
        date.setDate(date.getDate() - i)
        const label = date.toLocaleDateString("en-US", { weekday: "short" })
        labels.push(label)
        counts[label] = 0
      }
    } else if (timeframe === "month") {
      for (let i = 29; i >= 0; i--) {
        const date = new Date(now)
        date.setDate(date.getDate() - i)
        const label = date.getDate()
        labels.push(label)
        counts[label] = 0
      }
    } else if (timeframe === "year") {
      for (let i = 11; i >= 0; i--) {
        const date = new Date(now)
        date.setMonth(date.getMonth() - i)
        const label = date.toLocaleDateString("en-US", { month: "short" })
        labels.push(label)
        counts[label] = 0
      }
    }

    // Count articles read on each date
    readArticles.forEach((article) => {
      const date = new Date(article.publishedAt || article.date || now)

      let label
      if (timeframe === "week") {
        label = date.toLocaleDateString("en-US", { weekday: "short" })
      } else if (timeframe === "month") {
        label = date.getDate()
      } else if (timeframe === "year") {
        label = date.toLocaleDateString("en-US", { month: "short" })
      }

      if (counts[label] !== undefined) {
        counts[label]++
      }
    })

    // Format for chart
    return labels.map((label) => ({
      name: label,
      articles: counts[label],
    }))
  }

  // Get reading activity data based on current timeframe
  const readingActivityData = getReadingActivityData()

  // Generate category data from read articles
  const getCategoryData = () => {
    const categories = {}

    readArticles.forEach((article) => {
      const category = article.category || "uncategorized"
      if (!categories[category]) {
        categories[category] = 0
      }
      categories[category]++
    })

    // Convert to array and sort by count
    return Object.entries(categories)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 5) // Top 5 categories
  }

  const categoryData = getCategoryData()

  // Source distribution data
  const getSourceData = () => {
    const sources = {}

    readArticles.forEach((article) => {
      const source = article.source?.name || article.source || "Unknown"
      if (!sources[source]) {
        sources[source] = 0
      }
      sources[source]++
    })

    // Convert to array and sort by count
    return Object.entries(sources)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 5) // Top 5 sources
  }

  const sourceData = getSourceData()

  // Saved vs Read ratio data
  const savedVsReadData = [
    { name: "Read", value: totalArticlesRead - totalArticlesSaved },
    { name: "Saved", value: totalArticlesSaved },
  ]

  // Colors for charts
  const COLORS = ["#6366f1", "#8b5cf6", "#ec4899", "#f43f5e", "#f97316"]

  // Format for day of week
  const formatDay = (day) => {
    return day
  }

  return (
    <div className="analytics-container">
      <h1 className="analytics-title">
        <FaChartBar /> Your Reading Analytics
      </h1>
      <p className="analytics-description">
        Track your reading habits and discover insights about your news consumption patterns.
      </p>

      {/* Stats Overview */}
      <div className="stats-overview">
        <div className="stat-card">
          <div className="stat-icon">
            <FaEye />
          </div>
          <div className="stat-content">
            <h3>{totalArticlesRead}</h3>
            <p>Articles Read</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <FaBookmark />
          </div>
          <div className="stat-content">
            <h3>{totalArticlesSaved}</h3>
            <p>Articles Saved</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <FaHashtag />
          </div>
          <div className="stat-content">
            <h3>{categoryData.length}</h3>
            <p>Categories Explored</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <FaNewspaper />
          </div>
          <div className="stat-content">
            <h3>{sourceData.length}</h3>
            <p>News Sources</p>
          </div>
        </div>
      </div>

      {/* Reading Activity Chart */}
      <div className="chart-card">
        <div className="chart-header">
          <h2>
            <FaRegClock /> Reading Activity
          </h2>
          <div className="timeframe-selector">
            <button className={timeframe === "week" ? "active" : ""} onClick={() => setTimeframe("week")}>
              Week
            </button>
            <button className={timeframe === "month" ? "active" : ""} onClick={() => setTimeframe("month")}>
              Month
            </button>
            <button className={timeframe === "year" ? "active" : ""} onClick={() => setTimeframe("year")}>
              Year
            </button>
          </div>
        </div>

        <div className="chart-container">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={readingActivityData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis
                dataKey="name"
                tickFormatter={timeframe === "week" ? formatDay : null}
                axisLine={false}
                tickLine={false}
              />
              <YAxis axisLine={false} tickLine={false} tickCount={5} />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="articles"
                name="Articles Read"
                stroke="#6366f1"
                activeDot={{ r: 8 }}
                strokeWidth={3}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Category & Source Distribution */}
      <div className="charts-row">
        <div className="chart-card half">
          <h2>
            <FaHashtag /> Top Categories
          </h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={categoryData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
                <XAxis type="number" axisLine={false} tickLine={false} />
                <YAxis
                  dataKey="name"
                  type="category"
                  axisLine={false}
                  tickLine={false}
                  width={100}
                  tick={{ transform: "translate(-5, 0)", textAnchor: "end" }}
                />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" name="Articles" fill="#6366f1" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-card half">
          <h2>
            <FaNewspaper /> Top Sources
          </h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={sourceData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                  nameKey="name"
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                >
                  {sourceData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Show no data message if no articles */}
      {readArticles.length === 0 && (
        <div className="no-data-message">
          <FaBookOpen className="no-data-icon" />
          <h3>No reading data yet</h3>
          <p>Start reading articles to see your analytics.</p>
        </div>
      )}
    </div>
  )
}

export default Analytics

