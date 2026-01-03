"""
Database Models for Agentic AI Backend
Defines the Meeting schema and other data models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

Base = declarative_base()


class Meeting(Base):
    """
    Meeting model for storing scheduled meetings
    """
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    scheduled_date = Column(DateTime, nullable=False, index=True)
    location = Column(String(255), nullable=True)
    weather_condition = Column(String(100), nullable=True)
    is_weather_dependent = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Meeting(id={self.id}, title='{self.title}', scheduled_date={self.scheduled_date})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "scheduled_date": self.scheduled_date.isoformat() if self.scheduled_date else None,
            "location": self.location,
            "weather_condition": self.weather_condition,
            "is_weather_dependent": self.is_weather_dependent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class DocumentMetadata(Base):
    """
    Document metadata for tracking uploaded documents
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)
    upload_date = Column(DateTime, server_default=func.now())
    processed = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "filepath": self.filepath,
            "file_type": self.file_type,
            "upload_date": self.upload_date.isoformat() if self.upload_date else None,
            "processed": self.processed,
        }
