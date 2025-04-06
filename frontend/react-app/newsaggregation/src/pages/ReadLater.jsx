import NewsFeed from "../components/NewsFeed"
import "./Today.css"

const ReadLater = ({ user }) => {
  return (
    <div className="today-container">
      <h2 className="today-title">Read Later Articles</h2>
      <p className="page-description">
        Articles you've saved for later reading. Take your time to explore these stories when it's convenient for you.
      </p>
      <div className="news-grid">
        <NewsFeed page="ReadLater" user={user} />
      </div>
    </div>
  )
}

export default ReadLater

