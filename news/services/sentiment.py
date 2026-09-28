import re
from textblob import TextBlob


def analyze_sentiment(text: str):
    clean = re.sub(r'\s+', ' ', (text or '')).strip()
    if not clean:
        return 'Neutral', 0.0

    polarity = TextBlob(clean).sentiment.polarity
    if polarity > 0.1:
        return 'Positive', round(float(polarity), 4)
    if polarity < -0.1:
        return 'Negative', round(float(polarity), 4)
    return 'Neutral', round(float(polarity), 4)
