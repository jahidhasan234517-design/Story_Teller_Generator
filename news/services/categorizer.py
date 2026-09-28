import re
from typing import Dict

CATEGORY_KEYWORDS: Dict[str, list[str]] = {
    'AI': ['artificial intelligence', 'machine learning', 'ai', 'llm', 'chatgpt', 'deep learning', 'neural network', 'gpt'],
    'Technology': ['software', 'computer', 'technology', 'cloud', 'developer', 'platform', 'startup', 'hardware', 'digital'],
    'Cybersecurity': ['security', 'cyber', 'malware', 'ransomware', 'hacking', 'breach', 'privacy', 'phishing'],
    'Finance': ['stock', 'market', 'bank', 'investment', 'finance', 'economy', 'trading', 'crypto', 'bitcoin'],
    'Health': ['health', 'medical', 'hospital', 'wellness', 'disease', 'vaccine', 'fitness'],
    'Science': ['science', 'research', 'climate', 'space', 'physics', 'biology', 'astronomy', 'lab'],
    'World': ['world', 'europe', 'asia', 'africa', 'government', 'policy', 'global'],
    'Programming': ['python', 'javascript', 'programming', 'code', 'developer', 'web', 'backend', 'frontend', 'api'],
    'Education': ['education', 'student', 'school', 'university', 'teaching', 'learning'],
    'Environment': ['environment', 'climate', 'sustainability', 'energy', 'green', 'carbon'],
    'Business': ['business', 'leadership', 'ceo', 'management', 'strategy', 'enterprise'],
}


def normalize_text(value: str) -> str:
    return re.sub(r'[^a-z0-9\s]', ' ', (value or '').lower())


def classify_category(text: str) -> str:
    normalized = normalize_text(text)
    if not normalized:
        return 'World'

    scores = {name: 0 for name in CATEGORY_KEYWORDS}
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalized:
                scores[category] += 2
    if not any(scores.values()):
        return 'World'
    return max(scores, key=scores.get)
