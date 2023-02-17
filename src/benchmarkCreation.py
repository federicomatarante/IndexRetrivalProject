from src.apii import Review
from src.docsmanager import DocsDatabase


# 1 OR QUERY
# 2 AND QUERY
# 3 Phrase Query

def or_query(reviews: list[Review], query: str) -> dict[str, int]:
    matches = {}
    for review in reviews:
        count = 0
        if any(word.lower() in review.product.lower() for word in query):
            count += 2 * sum(1 for word in query if word in review.product)
        if any(word.lower() in review.text.lower() for word in query):
            count += sum(1 for word in query if word in review.text)
        if count > 0:
            matches[review.document] = count
    return {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}


def and_query(reviews: list[Review], query: str) -> dict[str, int]:
    matches = {}
    for review in reviews:
        count = 0
        if all(word.lower() in review.product.lower() for word in query):
            count += 2
        if all(word.lower() in review.text.lower() for word in query):
            count += 1
        if count > 0:
            matches[review.document] = count
    return {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}


def phrasal_query(reviews: list[Review], query: str) -> dict[str, int]:
    matches = {}
    for review in reviews:
        count = 0
        if query.lower() in review.product.lower():
            count += 1
        if count > 0:
            matches[review.document] = count
    return {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}


def evaluateQuery(query, reviews) -> dict[str, int]:
    if query.startswith('&'):
        return and_query(reviews, query[1:])
    elif sum(1 for c in query if c == '"') == 2:
        return phrasal_query(reviews, query.replace('"', ''))
    else:
        return or_query(reviews, query)


def run():
    directory = "C:\\Users\\feder\\PycharmProjects\\IndexRetrivalProject\\src\\Doc"
    docsDatabase: DocsDatabase = DocsDatabase(directory)

    queries: list[str] = [
        "& iphone good camera",
        "& samsung cpu bad",
        "& battery low price",
        "Do not buy, it's bad!",
        "I love this product",
        "The CPU is bad, but the camera is good",
        "The camera is good, but the battery is bad",
        '"32GB"',
        '"samsung galaxy"',
        '"iphone"',
    ]

    results = dict()
    reviews = docsDatabase.getDocs()

    for query in queries:
        documents: dict[str, int] = evaluateQuery(query, reviews)
        results[query] = documents

    # Save results into a created file
    with open("results.txt", "w") as file:
        file.write(results.__str__())


if __name__ == "__main__":
    run()
