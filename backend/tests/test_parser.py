"""
Unit tests for Module 3: HTML Parser.
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.inspection import InspectionResult
from app.parser.html_parser import HTMLParser


def test_html_parser_extraction():
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title> Test Page Title </title>
        <meta name="description" content="This is a test meta description string." />
    </head>
    <body>
        <h1>Primary Heading</h1>
        <h2>Secondary Heading 1</h2>
        <h2>Secondary Heading 2</h2>
        <p>First paragraph text content with word count details.</p>
        <img src="/image1.jpg" alt="Description of image 1" />
        <img src="https://external.com/image2.png" />
        <a href="/internal-link">Internal Link</a>
        <a href="https://external.com/page">External Link</a>
    </body>
    </html>
    """

    inspection_result = InspectionResult(
        url="https://testsite.com",
        final_url="https://testsite.com",
        status_code=200,
        response_time_ms=150.0,
        html_content=sample_html
    )

    doc = HTMLParser.parse(inspection_result)

    assert doc.title == "Test Page Title"
    assert doc.meta_description == "This is a test meta description string."
    assert doc.headings["h1"] == ["Primary Heading"]
    assert len(doc.headings["h2"]) == 2
    assert len(doc.images) == 2
    assert doc.images[0].has_alt is True
    assert doc.images[1].has_alt is False
    assert len(doc.links) == 2
    assert doc.links[0].is_internal is True
    assert doc.links[1].is_internal is False
