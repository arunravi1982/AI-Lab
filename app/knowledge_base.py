import json

from app.config import KNOWLEDGE_FILE


def search_articles(query: str):

    with open(
        KNOWLEDGE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        articles = json.load(file)

    query_words = set(
        query.lower().split()
    )

    scored_results = []

    for article in articles:

        text = (
            article["topic"] + " " +
            article["content"]
        ).lower()

        article_words = set(text.split())

        score = len(
            query_words.intersection(article_words)
        )

        if score > 0:

            scored_results.append(
                (score, article)
            )

    scored_results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        article
        for score, article in scored_results[:3]
    ]
