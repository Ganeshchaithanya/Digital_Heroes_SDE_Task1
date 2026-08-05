"""
Model representing calculated quantitative feature vector.
"""
from pydantic import BaseModel, Field


class FeatureVector(BaseModel):
    title_length: int = 0
    meta_description_length: int = 0
    h1_count: int = 0
    h2_count: int = 0
    total_images_count: int = 0
    missing_alt_images_count: int = 0
    word_count: int = 0
    internal_links_count: int = 0
    external_links_count: int = 0
    response_time_ms: float = 0.0
    status_code: int = 0
    has_title: bool = False
    has_meta_description: bool = False
