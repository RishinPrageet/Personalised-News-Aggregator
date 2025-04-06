from pydantic import BaseModel

class ChatbotRequest(BaseModel):
    message: str
    article_id: int = None  # Optional field for article ID

class ChatbotResponse(BaseModel):
    reply: str