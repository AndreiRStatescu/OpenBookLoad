"""Novel and Chapter models for API responses."""
from typing import List
from pydantic import BaseModel, Field


class Chapter(BaseModel):
    """Represents a chapter of a novel."""
    
    number: int = Field(..., description="Chapter number/index")
    title: str = Field(..., description="Chapter title")
    url: str = Field(..., description="Full URL to the chapter")
    content: str = Field(default="", description="Chapter content/text")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "number": 1,
                    "title": "Chapter 1: The Beginning",
                    "url": "https://www.honeyfeed.fm/chapters/12345",
                    "content": "Once upon a time..."
                }
            ]
        }
    }


class Novel(BaseModel):
    """Represents a novel with its metadata and chapters."""
    
    title: str = Field(..., description="Novel title")
    novel_id: str = Field(..., description="Novel ID on the source platform")
    url: str = Field(..., description="Full URL to the novel page")
    chapters: List[Chapter] = Field(default_factory=list, description="List of chapters")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "My Awesome Novel",
                    "novel_id": "12345",
                    "url": "https://www.honeyfeed.fm/novels/12345",
                    "chapters": [
                        {
                            "number": 1,
                            "title": "Chapter 1: The Beginning",
                            "url": "https://www.honeyfeed.fm/chapters/12345",
                            "content": "Once upon a time..."
                        }
                    ]
                }
            ]
        }
    }
