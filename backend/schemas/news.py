from datetime import datetime
from typing import Optional
from pydantic import BaseModel,ConfigDict

class NewsResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    link: str
    image: Optional[str] = None
    published: datetime
    website_id: int
    model_config = ConfigDict(from_attributes=True) 


class FollowWebsiteRequest(BaseModel):
    website_id: int
class ReadLater(BaseModel):
    news_id: int