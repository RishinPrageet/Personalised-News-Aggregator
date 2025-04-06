"use client"

import { useNavigate } from "react-router-dom"
import {
  FaRss,
  FaUserCheck,
  FaBookmark,
  FaNewspaper,
  FaGlobe,
  FaChartLine,
  FaSearch,
  FaBell,
  FaArrowRight,
  FaRegLightbulb,
} from "react-icons/fa"
import "./HomePage.css"

const HomePage = ({ user }) => {
  const navigate = useNavigate()

  const features = [
    {
      icon: <FaNewspaper className="feature-icon" />,
      title: "Latest News",
      description: "Stay updated with breaking news and trending stories from around the world.",
    },
    {
      icon: <FaUserCheck className="feature-icon" />,
      title: "Personalized Feed",
      description: "Get news tailored to your interests based on your reading habits and preferences.",
    },
    {
      icon: <FaRss className="feature-icon" />,
      title: "Follow Sources",
      description: "Subscribe to your favorite news sources and never miss important updates.",
    },
    {
      icon: <FaBookmark className="feature-icon" />,
      title: "Save for Later",
      description: "Bookmark articles to read when you have time and keep track of what you've read.",
    },
  ]

  const categories = [
    { name: "Business", icon: <FaChartLine />, path: "/search?category=business" },
    { name: "Technology", icon: <FaGlobe />, path: "/search?category=technology" },
    { name: "Health", icon: <FaBell />, path: "/search?category=health" },
    { name: "Science", icon: <FaRegLightbulb />, path: "/search?category=science" },
    { name: "Sports", icon: <FaSearch />, path: "/search?category=sports" },
    { name: "Entertainment", icon: <FaNewspaper />, path: "/search?category=entertainment" },
  ]

  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1>Your Personalized News Experience</h1>
          <p>
            Get real-time, customized news updates from sources you trust. Follow topics that interest you and stay
            informed with our intelligent news aggregation platform.
          </p>

          {user ? (
            <div className="welcome-back">
              <h2>Welcome back, {user.username}!</h2>
              <div className="hero-buttons">
                <button className="primary-button" onClick={() => navigate("/today")}>
                  Today's News <FaArrowRight />
                </button>
                <button className="secondary-button" onClick={() => navigate("/ForYou")}>
                  Your Feed <FaUserCheck />
                </button>
              </div>
            </div>
          ) : (
            <div className="hero-buttons">
              <button className="primary-button" onClick={() => navigate("/today")}>
                Start Reading <FaArrowRight />
              </button>
              <button className="secondary-button" onClick={() => alert("Sign in functionality would go here")}>
                Sign In
              </button>
            </div>
          )}
        </div>
        <div className="hero-image">
          <img src="/placeholder.svg?height=400&width=500" alt="News Aggregator" />
        </div>
      </section>

      {/* Categories Section */}
      <section className="categories-section">
        <h2 className="section-title">Browse by Category</h2>
        <p className="section-description">Explore news from different categories that interest you</p>

        <div className="categories-grid">
          {categories.map((category, index) => (
            <div key={index} className="category-card" onClick={() => navigate(category.path)}>
              <div className="category-icon">{category.icon}</div>
              <h3>{category.name}</h3>
              <FaArrowRight className="arrow-icon" />
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <h2 className="section-title">Powerful Features</h2>
        <p className="section-description">Everything you need to stay informed in one place</p>

        <div className="features-grid">
          {features.map((feature, index) => (
            <div key={index} className="feature-card">
              {feature.icon}
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h2>Ready to customize your news experience?</h2>
          <p>Follow your favorite sources and start getting personalized news today.</p>
          <button className="cta-button" onClick={() => navigate("/follow-sources")}>
            <FaRss /> Start Following Sources
          </button>
        </div>
      </section>
    </div>
  )
}

export default HomePage

