import nltk
import gensim
# import numpy as np

import os


def tokenize(text):
    sent_tokens = nltk.tokenize.sent_tokenize(text)

    gen_docs = [[w.lower() for w in nltk.tokenize.word_tokenize(text)]
                for text in sent_tokens]

    return gen_docs

class SimilarityChecker:
    def __init__(self, language: str):
        with open(os.path.join('GDPR_summary', f"{language}.txt"), 'r') as file:
            gdpr_summary = file.read()
            gdpr_summary = tokenize(gdpr_summary)

        self.dictionary = gensim.corpora.Dictionary(gdpr_summary)
        corpus = [self.dictionary.doc2bow(gen_doc) for gen_doc in gdpr_summary]

        print(corpus)

        # create similarity measure object based on tfidf
        tf_idf = gensim.models.TfidfModel(corpus)


        sims = gensim.similarities.Similarity('idx_stored/', tf_idf[corpus],
                                              num_features=len(self.dictionary))


    def check_query_doc(self, text: str):
        tokens = nltk.tokenize.sent_tokenize(text)
        bow_docs = []
        for line in tokens:
            query_doc = [w.lower() for w in nltk.tokenize.word_tokenize(line)]
            query_doc_bow = self.dictionary.doc2bow(query_doc)
            bow_docs.append(query_doc_bow)


        print(bow_docs)


if __name__ == "__main__":
    sc = SimilarityChecker('en')
    sc.check_query_doc("hello I am. Undet the wate. lol.")
