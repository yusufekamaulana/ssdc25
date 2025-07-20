import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

def render_wordcloud_and_bigrams(df, selected_topic):
    topic_df = df[df["topic_simplified"] == selected_topic]
    texts = topic_df["review_comment_translated"].dropna().astype(str).tolist()

    # Combine all text
    text_blob = " ".join(texts)

    # Prepare wordcloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_blob)

    # Prepare bigrams
    vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words='english')
    X = vectorizer.fit_transform(texts)
    bigram_freq = X.sum(axis=0).A1
    bigrams = vectorizer.get_feature_names_out()
    bigram_count = dict(zip(bigrams, bigram_freq))
    top_bigrams = Counter(bigram_count).most_common(10)

    col1, col2 = st.columns(2)

    # WordCloud
    with col1:
        st.markdown("#### WordCloud")
        fig_wc, ax_wc = plt.subplots(figsize=(8, 4))
        ax_wc.imshow(wordcloud, interpolation='bilinear')
        ax_wc.axis("off")
        st.pyplot(fig_wc)

    # Bigram Chart
    with col2:
        st.markdown("#### Top 10 Most Frequent Words")
        if top_bigrams:
            bigram_labels, bigram_values = zip(*top_bigrams)
            fig_bg, ax_bg = plt.subplots(figsize=(8, 4))
            ax_bg.barh(bigram_labels[::-1], bigram_values[::-1], color="#764ba2")
            ax_bg.set_xlabel("Frequency")
            ax_bg.set_title("Top Bigrams")
            st.pyplot(fig_bg)
        else:
            st.info("No bigrams found for this topic.")
