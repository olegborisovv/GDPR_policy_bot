def preprocess_text(text: str) -> str:
    text = text.lower()
    # remove unnecessary white spaces
    text = " ".join(text.split())

    # TODO: possibly remove stopwords, tokenize text
    return text