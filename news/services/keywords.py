import re
from collections import Counter

STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'of', 'to', 'in', 'on', 'for', 'with', 'as', 'at', 'by', 'from', 'is', 'it',
    'this', 'that', 'be', 'are', 'was', 'were', 'has', 'have', 'will', 'us', 'our', 'you', 'your', 'they', 'them',
    'about', 'into', 'their', 'its', 'after', 'before', 'over', 'under', 'between', 'through', 'while', 'if', 'so',
    'we', 'can', 'but', 'not', 'no', 'yes', 'who', 'what', 'when', 'where', 'why', 'how', 'all', 'new', 'more',
    'one', 'two', 'three', 'such', 'than', 'then', 'there', 'these', 'those', 'using', 'used', 'also', 'most', 'many'
}


def extract_keywords(text: str, limit: int = 8):
    if not text:
        return []
    text = text.lower()
    words = re.findall(r"[a-z0-9]+", text)
    filtered = [word for word in words if word not in STOP_WORDS and len(word) > 2]
    counts = Counter(filtered)
    return [word for word, _ in counts.most_common(limit)]
