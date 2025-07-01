import re

def slugify_title(title: str) -> str:
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s]+', '-', slug).strip('-')
    return slug

# My first post
# my-first-post

def convert(doc):
    doc["id"] = str(doc.get("_id", ""))
    doc.pop("_id", None)
    return doc


