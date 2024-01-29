import streamlit as sl
from textblob import TextBlob
from newspaper import Article
from wordcloud import WordCloud
import matplotlib.pyplot as plt

sl.title("News Express")
sl.write("##")

with sl.form("News Details"):
    inp_url = sl.text_input("Enter the News URL")
    submit_btn = sl.form_submit_button("Search details")

sl.write("##")
sl.markdown("""-----""")


if submit_btn:
    article = Article(inp_url)
    article.download()
    article.parse()
    article.nlp()
    sl.write("## News Details:")
    sl.write(f"### {article.title}")
    sl.markdown("""-----""")
    sl.write("##")
    sl.image(article.top_image)
    sl.write("##")
    sl.write("### Full News:")
    sl.write(article.text)
    sl.markdown("""-----""")
    sl.write("##")
    sl.write("### News Summary:")
    sl.write(article.summary)
    sl.markdown("""-----""")
    sl.write("##")
    sl.write(f"### Published by {article.authors[0]}")
    sl.write(f"### Published on {article.publish_date}")
    sl.markdown("""-----""")
    sl.write("##")
    sl.write("### Important keywords:")
    news_keywords = ", ".join(article.keywords)
    sl.write(news_keywords)
    sl.markdown("""-----""")
    sl.write("##")
    sen_analysis = TextBlob(article.text)
    sl.write(f"### News Sentiment Analysis : {"Positive" if sen_analysis.polarity > 0 else "Negative" if sen_analysis.polarity < 0 else "Neutral"}")
    sl.markdown("""-----""")
    sl.write("##")
    sl.write("### News Word Cloud:")
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(article.text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    sl.pyplot(plt)
    sl.markdown("""-----""")
