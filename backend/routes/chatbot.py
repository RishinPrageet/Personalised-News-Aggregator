from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from backend.models.news import News
from backend.schemas.news import NewsResponse
from backend.models.website import Website

from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from backend.schemas.chatbot import ChatbotRequest, ChatbotResponse
import requests
from bs4 import BeautifulSoup
import torch
from backend.database.db import get_db

router = APIRouter(prefix="/api/chatbot")

# Load the summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)  # Force CPU usage

# Clear unused GPU memory
torch.cuda.empty_cache()

# Load the conversational model with fp16 precision
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium", torch_dtype=torch.float16 if device.type == "cuda" else torch.float32).to(device)

# Dynamically set the device for the pipeline
pipeline_device = 0 if device.type == "cuda" else -1
chat_model = pipeline("text-generation", model=model, tokenizer=tokenizer, device=pipeline_device)

@router.post("/", response_model=ChatbotResponse)
def chatbot_response(request: ChatbotRequest, db: Session = Depends(get_db)):
    user_message = request.message.lower()
    print(f"User message: {user_message}")
    print(f"Article ID: {request.article_id}")

    if request.article_id:
        # Fetch article details using the article ID
        print(f"Fetching article with ID: {request.article_id}")
        try:
            article_response = db.query(News).filter(News.id == request.article_id).first()
            if not article_response:
                raise HTTPException(status_code=404, detail="Article not found")
            
            # Convert the SQLAlchemy object to a Pydantic model
            article_response = NewsResponse(
                id=article_response.id,
                title=article_response.title,
                description=article_response.description,
                link=article_response.link,
                image=article_response.image,
                published=article_response.published,
                website_id=article_response.website_id
            )
            print(article_response)

            article_link = article_response.link

            if not article_link:
                raise HTTPException(status_code=400, detail="Article link is missing.")

            # Fetch the article content from the link
            webpage_response = requests.get(article_link)
            webpage_response.raise_for_status()
            soup = BeautifulSoup(webpage_response.text, "html.parser")
            paragraphs = soup.find_all("p")
            article_text = " ".join([p.get_text() for p in paragraphs])

            if not article_text.strip():
                raise HTTPException(status_code=400, detail="Failed to extract content from the article link.")

            # List of phrases that indicate a summary intent
            summary_intents = [
                "summarize", "summary", "shorten", "tl;dr", "gist", "in short", 
                "brief", "quick recap", "recap", "can you sum", "give me the short", 
                "tell me the main points", "main idea", "core idea"
            ]

            # Check if any intent phrase exists in user message
            if any(phrase in user_message for phrase in summary_intents):
                summary = summarizer(article_text, max_length=150, min_length=80, do_sample=False)
                return ChatbotResponse(reply=summary[0]["summary_text"])
            else:
                return ChatbotResponse(reply="I found the article. Let me know if you'd like me to summarize it.")

        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching article: {str(e)}")

    # Handle casual chat using the conversational model
    try:
        chat_response = chat_model(user_message, max_length=50, num_return_sequences=1)
        return ChatbotResponse(reply=chat_response[0]["generated_text"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
