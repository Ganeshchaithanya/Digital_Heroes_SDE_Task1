"""
SEO Feature Extractor.
Extracts title length, meta description length, heading counts.
"""
from typing import Dict, Any
from app.models.document import PageDocument


class SEOFeatureExtractor:
    """
    Extracts SEO specific quantitative metrics from PageDocument.
    """

    @staticmethod
    def extract(document: PageDocument) -> Dict[str, Any]:
        title = document.title or ""
        meta_desc = document.meta_description or ""
        h1_list = document.headings.get("h1", [])
        h2_list = document.headings.get("h2", [])

        return {
            "title_length": len(title),
            "meta_description_length": len(meta_desc),
            "h1_count": len(h1_list),
            "h2_count": len(h2_list),
            "has_title": bool(title),
            "has_meta_description": bool(meta_desc)
        }
