import streamlit as sl
import matplotlib.pyplot as plt
import spacy
from textblob import TextBlob
from newspaper import Article
from wordcloud import WordCloud

nlp = spacy.load("en_core_web_sm")

sl.title("News Express")
sl.write("##")


def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


with sl.form("News Details"):
    inp_url = sl.text_input("Enter the News URL")
    submit_btn = sl.form_submit_button("Search details")

sl.write("##")
sl.markdown("""-----""")

if submit_btn:
    try:
        article = Article(inp_url)
        article.download()
        article.parse()
        article.nlp()

        if not article.title:
            sl.warning("No title found for the article.")
            sl.stop()

        ner_entities = extract_entities(article.text)
        entity_colors = {
            "PERSON": "#87CEEB",
            "ORG": "#00FF00",
            "LOC": "#FF0000",
            "NORP": "#FFA500",
        }
        sl.write("## News Details:")
        sl.write(f"### {article.title}")
        sl.markdown("""-----""")

        sl.write("##")
        sl.image(article.top_image)

        sl.write("##")
        sl.write("### Full News:")
        highlighted_text = article.text
        for entity, label in ner_entities:
            color = entity_colors.get(label, "white")
            highlighted_text = highlighted_text.replace(
                entity,
                f"<span style='color: {color}; font-weight: bold;'>{entity}</span>",
                1,
            )
        sl.markdown(highlighted_text, unsafe_allow_html=True)
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
        sl.write(
            f"### News Sentiment Analysis : {'Positive' if sen_analysis.polarity > 0 else 'Negative' if sen_analysis.polarity < 0 else 'Neutral'}"
        )
        sl.markdown("""-----""")

        sl.write("##")
        sl.write("### News Word Cloud:")
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            article.text
        )
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        sl.pyplot(plt)
        sl.markdown("""-----""")

        sl.write("##")
        sl.write("### Named Entity Recognition (NER):")
        sl.write("###")
        ner_entities = extract_entities(article.text)
        filtered_entities = [
            (entity, label)
            for entity, label in ner_entities
            if label in ["NORP", "PERSON", "ORG", "LOC"]
        ]
        custom_order = ["ORG", "PERSON", "LOC", "NORP"]
        sorted_entities = sorted(
            filtered_entities, key=lambda x: custom_order.index(x[1])
        )
        org_keys = []
        person_keys = []
        loc_keys = []
        norp_keys = []
        for entity, label in sorted_entities:
            if label == "ORG":
                org_keys.append(entity)
            elif label == "PERSON":
                person_keys.append(entity)
            elif label == "LOC":
                loc_keys.append(entity)
            else:
                norp_keys.append(entity)

        if not any([org_keys, person_keys, loc_keys, norp_keys]):
            sl.warning("No named entities found in the specified categories.")
        else:
            sl.write("**Organisations listed :**")
            sl.write(", ".join(org_keys))
            sl.write("###")
            sl.write("**Persons listed :**")
            sl.write(", ".join(person_keys))
            sl.write("###")
            sl.write("**Locations listed :**")
            sl.write(", ".join(loc_keys))
            sl.write("###")
            sl.write("**Places listed :**")
            sl.write(", ".join(norp_keys))

        sl.markdown("""-----""")

    except Exception as e:
        sl.error("An error occurred. Enter the correct URL")
