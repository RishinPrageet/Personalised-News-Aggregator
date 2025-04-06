from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.database.base import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, ForeignKey("news.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment = Column(Text, nullable=False)

    news = relationship("News", back_populates="comments")
    user = relationship("User", back_populates="comments")

    def to_dict(self):
        return {
            "id": self.id,
            "news_id": self.news_id,
            "user_id": self.user_id,
            "comment": self.comment
        }
