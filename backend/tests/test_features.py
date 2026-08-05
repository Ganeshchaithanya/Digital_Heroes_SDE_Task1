"""
Unit tests for Module 4: Feature Extractor.
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.document import PageDocument, ImageInfo, LinkInfo
from app.models.inspection import InspectionResult
from app.features.extractor import FeatureExtractor


def test_feature_extractor():
    doc = PageDocument(
        title="This Title is Thirty Characters Long!",
        meta_description="Sample description string",
        headings={"h1": ["Single Main Title"], "h2": ["Sub 1", "Sub 2"]},
        paragraphs=["Paragraph text here."],
        images=[
            ImageInfo(src="img1.jpg", alt="Alt text", has_alt=True),
            ImageInfo(src="img2.jpg", alt=None, has_alt=False)
        ],
        links=[
            LinkInfo(href="https://testsite.com/a", is_internal=True),
            LinkInfo(href="https://google.com", is_internal=False)
        ],
        raw_text="Hello world this is a test document with eight words."
    )

    inspection = InspectionResult(
        url="https://testsite.com",
        final_url="https://testsite.com",
        status_code=200,
        response_time_ms=450.5
    )

    fv = FeatureExtractor.extract_features(doc, inspection)

    assert fv.title_length == len("This Title is Thirty Characters Long!")
    assert fv.h1_count == 1
    assert fv.h2_count == 2
    assert fv.total_images_count == 2
    assert fv.missing_alt_images_count == 1
    assert fv.internal_links_count == 1
    assert fv.external_links_count == 1
    assert fv.response_time_ms == 450.5
    assert fv.status_code == 200
    assert fv.has_title is True
