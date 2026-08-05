"""
HTML Parser Module.
Parses raw HTML using BeautifulSoup4 / lxml and extracts document elements.
Does NOT perform evaluation or metric scoring.
"""
from typing import List, Dict
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from app.models.inspection import InspectionResult
from app.models.document import PageDocument, ImageInfo, LinkInfo
from app.shared.helpers import clean_text
from app.observability.logger import logger


class HTMLParser:
    """
    Parses raw HTML into a structured PageDocument object.
    """

    @staticmethod
    def parse(inspection_result: InspectionResult) -> PageDocument:
        html = inspection_result.html_content or ""
        base_url = inspection_result.final_url or inspection_result.url
        base_domain = urlparse(base_url).netloc.lower()

        try:
            soup = BeautifulSoup(html, "lxml")
        except Exception:
            # Fallback to default html.parser if lxml fails
            soup = BeautifulSoup(html, "html.parser")

        # 1. Extract Title
        title_tag = soup.find("title")
        title = clean_text(title_tag.string) if title_tag and title_tag.string else None

        # 2. Extract Meta Description
        meta_desc = None
        meta_tag = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "description"})
        if meta_tag and meta_tag.get("content"):
            meta_desc = clean_text(str(meta_tag.get("content")))

        # 3. Extract Headings (h1 through h6)
        headings: Dict[str, List[str]] = {}
        for h_level in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            found = soup.find_all(h_level)
            headings[h_level] = [clean_text(tag.get_text()) for tag in found if clean_text(tag.get_text())]

        # 4. Extract Paragraphs & Raw Text Body
        paragraphs: List[str] = []
        for p in soup.find_all("p"):
            txt = clean_text(p.get_text())
            if txt:
                paragraphs.append(txt)

        # Extract overall visible body text for word count
        body = soup.find("body") or soup
        raw_text = clean_text(body.get_text(separator=" "))

        # 5. Extract Images
        images: List[ImageInfo] = []
        for img in soup.find_all("img"):
            src = img.get("src") or ""
            if src:
                full_src = urljoin(base_url, src)
                alt = img.get("alt")
                alt_cleaned = clean_text(alt) if alt is not None else None
                has_alt = bool(alt_cleaned)
                images.append(ImageInfo(
                    src=full_src,
                    alt=alt_cleaned,
                    has_alt=has_alt
                ))

        # 6. Extract Links
        links: List[LinkInfo] = []
        for a in soup.find_all("a", href=True):
            href = a.get("href") or ""
            if href and not href.startswith(("javascript:", "mailto:", "tel:", "#")):
                full_href = urljoin(base_url, href)
                link_domain = urlparse(full_href).netloc.lower()
                is_internal = (link_domain == base_domain or link_domain == "")
                link_text = clean_text(a.get_text())
                links.append(LinkInfo(
                    href=full_href,
                    text=link_text,
                    is_internal=is_internal
                ))

        logger.info(
            f"Parsed HTML page - Title: '{title}', H1s: {len(headings.get('h1', []))}, "
            f"Images: {len(images)}, Links: {len(links)}"
        )

        return PageDocument(
            title=title,
            meta_description=meta_desc,
            headings=headings,
            paragraphs=paragraphs,
            images=images,
            links=links,
            raw_text=raw_text
        )
