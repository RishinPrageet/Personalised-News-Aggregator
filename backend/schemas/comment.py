from pydantic import BaseModel,ConfigDict

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    news_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
