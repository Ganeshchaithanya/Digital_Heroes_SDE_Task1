"""
Content & Accessibility Feature Extractor.
Extracts word count, link counts, and image ALT coverage metrics.
"""
from typing import Dict, Any
from app.models.document import PageDocument
from app.shared.helpers import count_words


class ContentFeatureExtractor:
    """
    Extracts content and accessibility quantitative metrics from PageDocument.
    """

    @staticmethod
    def extract(document: PageDocument) -> Dict[str, Any]:
        total_images = len(document.images)
        missing_alt = sum(1 for img in document.images if not img.has_alt)
        
        internal_links = sum(1 for link in document.links if link.is_internal)
        external_links = sum(1 for link in document.links if not link.is_internal)

        word_count = count_words(document.raw_text)

        return {
            "total_images_count": total_images,
            "missing_alt_images_count": missing_alt,
            "word_count": word_count,
            "internal_links_count": internal_links,
            "external_links_count": external_links
        }
