import NewsFeed from "../components/NewsFeed"
import "./Today.css"

const ForYou = ({ user }) => {
  return (
    <div className="today-container">
      <h2 className="today-title">For You</h2>
      <p className="page-description">
        {user
          ? `Welcome ${user.username}! Here's your personalized news feed based on your interests and reading habits.`
          : "Sign in to get personalized news recommendations based on your interests and reading habits."}
      </p>
      <div className="news-grid">
        <NewsFeed page="ForYou" user={user} />
      </div>
    </div>
  )
}

export default ForYou

