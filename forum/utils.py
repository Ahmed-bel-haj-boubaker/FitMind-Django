from textblob import TextBlob
import emoji

def analyse_sentiment_emoji(message):
    analysis = TextBlob(message)
    polarity = analysis.sentiment.polarity

    if polarity > 0.5:
        return "\U0001F603 Positive"  # 😃
    elif polarity > 0:
        return "\U0001F642 Slightly Positive"  # 🙂
    elif polarity == 0:
        return "\U0001F610 Neutral"  # 😐
    elif polarity > -0.5:
        return "\U0001F641 Slightly Negative"  # 🙁
    else:
        return "\U0001F620 Negative"  # 😡"