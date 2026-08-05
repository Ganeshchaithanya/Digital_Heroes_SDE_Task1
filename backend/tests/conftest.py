"""
Pytest configuration and test HTML fixtures.
"""
import pytest


@pytest.fixture
def healthy_website_html():
    """
    Healthy Website HTML:
    - Ideal title length (42 chars: 'PAGEPULSE - Modern Web Inspection Engine')
    - Meta description (110 chars)
    - Exactly 1 H1 tag
    - All content images have ALT tags
    - Word count > 300 words
    """
    paragraphs = " ".join([f"This is a high quality article paragraph number {i} providing detailed website metrics documentation." for i in range(25)])
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>PAGEPULSE - Modern Web Inspection Engine</title>
        <meta name="description" content="PAGEPULSE is a high performance deterministic website inspection platform built with FastAPI and React.">
    </head>
    <body>
        <h1>Website Health Inspection Standards</h1>
        <h2>Overview and Metrics</h2>
        <p>{paragraphs}</p>
        <img src="/logo.png" alt="PAGEPULSE Platform Logo">
        <img src="/icon.svg" alt="" role="presentation">
    </body>
    </html>
    """


@pytest.fixture
def non_healthy_seo_html():
    """
    Non-Healthy Website Case 1 (SEO & Content Failures):
    - Short title (8 chars: 'Bad Title')
    - Missing meta description (0 chars)
    - Multiple H1 tags (4 H1 tags)
    - Very low word count (12 words)
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bad Title</title>
    </head>
    <body>
        <h1>First Main Heading</h1>
        <h1>Second Confusing H1</h1>
        <h1>Third H1 Tag</h1>
        <h1>Fourth H1 Tag</h1>
        <p>Short snippet text only.</p>
    </body>
    </html>
    """


@pytest.fixture
def non_healthy_accessibility_html():
    """
    Non-Healthy Website Case 2 (Accessibility Failures):
    - Missing ALT text on multiple content images (5 missing ALT tags)
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sample Site with Accessibility Issues</title>
        <meta name="description" content="This site contains missing image alternative descriptions.">
    </head>
    <body>
        <h1>Accessibility Inspection Case</h1>
        <p>Testing accessibility parser with missing image alt attributes across multiple content images.</p>
        <img src="/img1.jpg">
        <img src="/img2.jpg">
        <img src="/img3.jpg">
        <img src="/img4.jpg">
        <img src="/img5.jpg">
    </body>
    </html>
    """
