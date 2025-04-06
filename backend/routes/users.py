
from fastapi import APIRouter, Depends, HTTPException,Request,status,Query
from fastapi.responses import RedirectResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import insert, delete, select,or_
from backend.database.db import get_db
from backend.models.user import User  # Import the User model
from backend.models.news import News
from backend.models.association import user_website,read_later
from backend.models.website import Website
from backend.schemas.user import UserCreate,UserResponse
from backend.schemas.news import FollowWebsiteRequest,ReadLater
from backend.utilities.hashing import hash_password
from backend.routes.auth import get_current_user
from jinja2 import Environment, FileSystemLoader
from fastapi.templating import Jinja2Templates
import os 
templates = Jinja2Templates(directory="frontend/templates")
react_template=Jinja2Templates(directory='frontend/react-app/newsaggregation/dist')

router=APIRouter(prefix="/user")

react_app_path = os.path.join("frontend", "react-app", "newsaggregation", "dist")
if not os.path.exists(react_app_path):
    raise RuntimeError("React app not found at path: " + react_app_path)



@router.get("/profile")
def get_user_profile(request: Request,current_user: UserResponse = Depends(get_current_user)):
    print("near_end")
    print("near_end")
    user={}
    user["id"]=current_user.id
    user['username']=current_user.username
    print(user)
    print(current_user)
    return react_template.TemplateResponse("index.html", {"request": request, "user": user})

@router.get("/me", response_model=UserResponse)
def get_current_user_data(current_user: UserResponse = Depends(get_current_user)):
    return current_user
@router.api_route('/logout',methods=["POST","GET"])
def logout(request: Request):
  
    response = RedirectResponse(url="/login")

    response.delete_cookie("access_token")
    return response



@router.post("/add_source", status_code=status.HTTP_201_CREATED)
def follow_website(
    request: FollowWebsiteRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Check if website exists
    website = db.query(Website).filter(Website.id == request.website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    # Check if already followed
    exists = db.execute(
        select(user_website).where(
            (user_website.c.user_id == current_user.id) &
            (user_website.c.website_id == request.website_id)
        )
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Already following this website")

    # Insert into association table
    db.execute(insert(user_website).values(user_id=current_user.id, website_id=request.website_id))
    db.commit()
    return {"message": "Website followed successfully"}

@router.post("/add_read", status_code=status.HTTP_201_CREATED)
def add_read(
    request: ReadLater,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Check if website exists
    print(request)
    news = db.query(News).filter(News.id == request.news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Website not found")

    # Check if already followed
    exists = db.execute(
        select(read_later).where(
            (read_later.c.user_id == current_user.id) &
            (read_later.c.news_id == request.news_id)
        )
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Already following this website")

    # Insert into association table
    db.execute(insert(read_later).values(user_id=current_user.id, news_id=request.news_id))
    db.commit()
    return {"message": "Website followed successfully"}
@router.delete("/remove_read", status_code=status.HTTP_200_OK)
def remove_read(
    request: ReadLater,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Check if the website exists in the user's read later list
    exists = db.execute(
        select(read_later).where(
            (read_later.c.user_id == current_user.id) &
            (read_later.c.news_id == request.news_id)
        )
    ).first()

    if not exists:
        raise HTTPException(status_code=404, detail="Website not found in read later list")

    # Delete the entry from read_later
    db.execute(
        delete(read_later).where(
            (read_later.c.user_id == current_user.id) &
            (read_later.c.news_id == request.news_id)
        )
    )
    db.commit()
    
    return {"message": "Website removed from read later"}


@router.delete("/remove_source", status_code=status.HTTP_200_OK)
def unfollow_website(
    request: FollowWebsiteRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Check if the follow record exists
    exists = db.execute(
        select(user_website).where(
            (user_website.c.user_id == current_user.id) &
            (user_website.c.website_id == request.website_id)
        )
    ).first()

    if not exists:
        raise HTTPException(status_code=404, detail="Not following this website")

    # Delete from association table
    db.execute(
        delete(user_website).where(
            (user_website.c.user_id == current_user.id) &
            (user_website.c.website_id == request.website_id)
        )
    )
    db.commit()
    return {"message": "Website unfollowed successfully"}

@router.get("/followed_sources", status_code=status.HTTP_200_OK)
def get_followed_websites(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    followed_websites = db.execute(
        select(Website).join(user_website, Website.id == user_website.c.website_id)
        .where(user_website.c.user_id == current_user.id)
    ).scalars().all()

    return followed_websites
@router.get("/read_later", status_code=status.HTTP_200_OK)
def get_followed_websites(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    followed_websites = db.execute(
        select(News).join(read_later, News.id == read_later.c.news_id)
        .where(read_later.c.user_id == current_user.id)
    ).scalars().all()

    return followed_websites
@router.delete("/remove_read_later", status_code=status.HTTP_200_OK)
def unfollow_website(
    request: ReadLater,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Check if the follow record exists
    exists = db.execute(
        select(News).where(
            (read_later.c.user_id == current_user.id) &
            (read_later.c.news_id == request.news_id)
        )
    ).first()

    if not exists:
        raise HTTPException(status_code=404, detail="Not saved ")

    # Delete from association table
    db.execute(
        delete(read_later).where(
            (read_later.c.user_id == current_user.id) &
            (read_later.c.news_id == request.news_id)
        )
    )
    db.commit()
    return {"message": "Website unfollowed successfully"}


@router.get("/news", status_code=status.HTTP_200_OK)
def get_user_news(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Get the list of website IDs followed by the user
    followed_websites = db.execute(
        select(Website.id)
        .join(user_website, Website.id == user_website.c.website_id)
        .where(user_website.c.user_id == current_user.id)
    ).scalars().all()

    if not followed_websites:
        return {"message": "No followed sources found."}

    # Retrieve news articles from these followed websites, sorted by date
    news_articles = db.execute(
        select(News)
        .where(News.website_id.in_(followed_websites))
        .order_by(News.published.desc())  # Sort by newest first
    ).scalars().all()

    return news_articles if news_articles else {"message": "No news available."}
@router.get("/search", status_code=status.HTTP_200_OK)
def search_news(q: str, db: Session = Depends(get_db)):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")

    words = q.split()  # Splitting the search query into words
    filters = [
        or_(
            News.title.ilike(f"%{word}%"),
            News.description.ilike(f"%{word}%")
        ) for word in words
    ]

    articles = db.query(News).filter(or_(*filters)).order_by(News.published.desc()).all()
    
    if not articles:
        raise HTTPException(status_code=404, detail="No matching articles found")

    return articles

