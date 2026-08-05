"""
Model representing parsed HTML document structure.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ImageInfo(BaseModel):
    src: str
    alt: Optional[str] = None
    has_alt: bool = False


class LinkInfo(BaseModel):
    href: str
    text: str = ""
    is_internal: bool = False


class PageDocument(BaseModel):
    title: Optional[str] = None
    meta_description: Optional[str] = None
    headings: Dict[str, List[str]] = Field(default_factory=dict)  # e.g. {"h1": [...], "h2": [...]}
    paragraphs: List[str] = Field(default_factory=list)
    images: List[ImageInfo] = Field(default_factory=list)
    links: List[LinkInfo] = Field(default_factory=list)
    raw_text: str = ""
