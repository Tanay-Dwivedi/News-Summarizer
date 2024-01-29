from textblob import TextBlob
from newspaper import Article

url = "https://edition.cnn.com/2024/01/28/politics/us-troops-hostages-gaza-ceasefire/index.html"

article = Article(url)

article.download()
article.parse()

article.nlp()

print(f"News: {article.text}")
print(f"Title: {article.title}")
print(f"Authors: {article.authors}")
print(f"Publicatin Date: {article.publish_date}")
print(f"Summary: {article.summary}")
print(article.keywords)

sen_analysis = TextBlob(article.text)
print(sen_analysis.polarity)

print(f"Sentiment: {"Positive" if sen_analysis.polarity > 0 else "Negative" if sen_analysis.polarity < 0 else "Neutral"}")


