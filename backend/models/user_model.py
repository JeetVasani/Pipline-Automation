from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.db import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    github = relationship("GitHubUser", back_populates="user", uselist=False)


class GitHubUser(Base):
    __tablename__ = "github_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    github_id = Column(Integer, unique=True, index=True)
    login = Column(String, unique=True, index=True)
    access_token = Column(String)
    name = Column(String)
    avatar_url = Column(String)

    user = relationship("User", back_populates="github")



class IssueCache(Base):
    __tablename__ = "issue_cache"

    id = Column(Integer, primary_key=True, index=True)
    repo = Column(String, index=True)
    number = Column(Integer, index=True)
    updated_at = Column(DateTime)
    title = Column(String)
    state = Column(String)
