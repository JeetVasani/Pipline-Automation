from fastapi import APIRouter, Depends

import httpx
from sqlalchemy.orm import Session

from api_services.github.github_services import get_user_profile
from db.db import SessionLocal
from models.user_model import GitHubUser, User
from api_services.github.oauth import exchange_code

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/repos/{username}")
async def get_repos(username: str, db: Session = Depends(get_db)):
    gh_user = db.query(GitHubUser).filter_by(login=username).first()
    if not gh_user:
        return []

    headers = {"Authorization": f"Bearer {gh_user.access_token}"}

    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://api.github.com/users/{username}/repos",
            headers=headers
        )
        return r.json()


@router.get("/user/{username}")
def get_full_user(username: str, db: Session = Depends(get_db)):
    gh_user = db.query(GitHubUser).filter_by(login=username).first()

    if not gh_user:
        return {"error": "not found"}

    return {
        "internal_id": gh_user.user.id,
        "email": gh_user.user.email,
        "github": {
            "login": gh_user.login,
            "avatar_url": gh_user.avatar_url,
            "name": gh_user.name
        }
    }


@router.get("/me/{login}")
def get_user(login: str, db: Session = Depends(get_db)):
    user = db.query(GitHubUser).filter_by(login=login).first()
    if not user:
        return {"error": "User not found"}

    return {
        "profile": {
            "login": user.login,
            "name": user.name,
            "avatar_url": user.avatar_url
        }
    }

# only for github
@router.get("/auth/callback")
async def auth_callback(code: str, db: Session = Depends(get_db)):
    token_data = exchange_code(code)
    access_token = token_data.get("access_token")

    if not access_token:
        return {"error": "Token exchange failed", "details": token_data}

    gh = await get_user_profile(access_token)

    login = gh["login"]
    github_id = gh["id"]

    existing_gh = db.query(GitHubUser).filter_by(github_id=github_id).first()

    if existing_gh:
        existing_gh.access_token = access_token
        db.commit()
        db.refresh(existing_gh)
        return {"status": "ok", "user": gh}

    new_user = User()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    gh_user = GitHubUser(
        user_id=new_user.id,
        github_id=github_id,
        login=login,
        access_token=access_token,
        name=gh.get("name"),
        avatar_url=gh.get("avatar_url")
    )

    db.add(gh_user)
    db.commit()

    return {"status": "ok", "user": gh}
