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
            soup = BeautifulSoup(html, "html.parser")

        # 1. Extract Title
        title_tag = soup.find("title")
        title = clean_text(title_tag.string) if title_tag and title_tag.string else None

        # 2. Extract Meta Description
        meta_desc = None
        meta_tag = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "description"})
        if meta_tag and meta_tag.get("content"):
            meta_desc = clean_text(str(meta_tag.get("content")))

        # 3. Canonical Tag & Robots Meta Tag
        canonical_tag = soup.find("link", attrs={"rel": lambda x: x and "canonical" in x.lower()})
        has_canonical = bool(canonical_tag and canonical_tag.get("href"))

        robots_tag = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "robots"})
        has_robots = bool(robots_tag)

        # 4. Extract Headings (h1 through h6)
        headings: Dict[str, List[str]] = {}
        for h_level in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            found = soup.find_all(h_level)
            headings[h_level] = [clean_text(tag.get_text()) for tag in found if clean_text(tag.get_text())]

        # 5. Extract Paragraphs & Raw Text Body
        paragraphs: List[str] = []
        for p in soup.find_all("p"):
            txt = clean_text(p.get_text())
            if txt:
                paragraphs.append(txt)

        body = soup.find("body") or soup
        raw_text = clean_text(body.get_text(separator=" "))

        # 6. Smart Image Extraction (Differentiating Decorative & Missing ALT)
        images: List[ImageInfo] = []
        for img in soup.find_all("img"):
            raw_src = img.get("src")
            src = (raw_src[0] if isinstance(raw_src, list) else raw_src) or ""
            if src and isinstance(src, str):
                full_src = urljoin(base_url, src)
                raw_alt = img.get("alt")
                alt_attr = (raw_alt[0] if isinstance(raw_alt, list) else raw_alt)
                
                raw_role = img.get("role")
                role_val = (raw_role[0] if isinstance(raw_role, list) else raw_role) or ""
                role_attr = role_val.lower() if isinstance(role_val, str) else ""

                raw_aria = img.get("aria-hidden")
                aria_val = (raw_aria[0] if isinstance(raw_aria, list) else raw_aria) or ""
                aria_hidden = (aria_val.lower() == "true") if isinstance(aria_val, str) else False

                # Check if image is decorative (alt="", role="presentation", role="none", aria-hidden="true")
                is_decorative = (alt_attr == "") or (role_attr in ["presentation", "none"]) or aria_hidden
                
                alt_str = alt_attr if isinstance(alt_attr, str) else (" ".join(alt_attr) if isinstance(alt_attr, list) else None)
                alt_cleaned = clean_text(alt_str) if alt_str is not None else None
                has_alt = bool(alt_cleaned) or is_decorative

                images.append(ImageInfo(
                    src=full_src,
                    alt=alt_cleaned,
                    has_alt=has_alt,
                    is_decorative=is_decorative
                ))

        # 7. Extract Links
        links: List[LinkInfo] = []
        for a in soup.find_all("a", href=True):
            raw_href = a.get("href")
            href = (raw_href[0] if isinstance(raw_href, list) else raw_href) or ""
            if href and isinstance(href, str) and not href.startswith(("javascript:", "mailto:", "tel:", "#")):
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
            f"Images: {len(images)} (Decorative: {sum(1 for i in images if i.is_decorative)}), Links: {len(links)}"
        )

        return PageDocument(
            title=title,
            meta_description=meta_desc,
            headings=headings,
            paragraphs=paragraphs,
            images=images,
            links=links,
            raw_text=raw_text,
            has_canonical=has_canonical,
            has_robots_meta=has_robots
        )
