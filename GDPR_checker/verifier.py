import flair
import re
import os
import nltk

# from .similarity_checker import SimilarityChecker
from GDPR_checker.similarity_checker import SimilarityChecker
from GDPR_checker.utils import preprocess_text

class GDPR_Verifier:
    def __init__(self, language: 'str', exact_match_threshold: "threshold for confidence level in meeting GDPR overlap" = 0.95,
                 window_size: int = 50):
        """

        :param exact_match_threshold: threshold for accepting how much positive the sentence is about GDPR policy
        :param window_size: if you peak large window size then the system will select the sentence where GDPR is
        reffered to
        """

        self.language = language
        self.exact_match_threshold = exact_match_threshold

        # For english language I choose `en` for any other choose appropriate letters
        # or train a new sentiment model for other language
        self.flair_sentiment = flair.models.TextClassifier.load('en-sentiment')
        self.window_size = window_size


    def _subtext(self, text: str, gdpr: str, initial_idx: int, window_size: int) -> str:
        """
        Will extract a subtext from any text, given a window_size as number of words to be included
        :param text: input text
        :param skip_chars_ahead: chars ahead to be skipped and not counted
        :param window_size: number of words to be included
        :return: subtext
        """
        # introduce special token (will help to avoid confusing two terminologies appearing close to each other
        # in the same text)
        GDPR_START_TOKEN = "<GDPR>"
        text = text[:initial_idx] + f" {GDPR_START_TOKEN} " + text[initial_idx:]

        # text = text.replace(".", " . ")

        # now we would like to only focus on the words neighbouring corresponding to our window size
        text = text.split()

        # first find our special token
        initial_idx = text.index(GDPR_START_TOKEN)

        # then go back either until we reach a full stop or until we have counted needed words
        start_idx = initial_idx
        for _ in range(window_size):
            if start_idx <= 0:
                break
            elif text[start_idx].endswith('.'):
                start_idx += 1
                break
            else:
                start_idx -= 1

        # now check for the end index similarly, either until we encounter full stop or counted all words

        # end_idx = min(len(text), initial_idx + window_size + len(gdpr.split())) + 1
        end_idx = initial_idx + len(gdpr.split())
        for _ in range(window_size):
            if end_idx >= len(text):
                break
            elif text[end_idx].endswith('.'):
                break
            else:
                end_idx += 1

        end_idx += 1

        res = text[start_idx:end_idx]
        res.remove(GDPR_START_TOKEN)

        return " ".join(res)

        pass

    def _sentence_sentiment(self, text: str):
        s = flair.data.Sentence(text)
        self.flair_sentiment.predict(s)
        total_sentiment = s.labels
        return total_sentiment[0].to_dict()

    def check_exact_overlap(self, policy_text: str, window_size) -> bool:
        """
        :param policy_text: input policy text
        :return: True if exact GDPR compiency text was found
        """
        # TODO: create list of overlaps with different versions how GDPR can be written
        gdpr_names = ["gdpr", "general eu data protection regulation", "general data protection regulation"]

        for gdpr in gdpr_names:
            if gdpr in policy_text:
                start_indices = [m.start() for m in re.finditer(gdpr, policy_text)]

                # now once we have all occurrences of gdpr text in the text we can go through each example
                # and to evaluate using sentiment analysis if GDPR is used in some positive form by using
                # a window of some size e.g. 5 words.
                for idx in start_indices:
                    text_chunk = self._subtext(policy_text, gdpr, initial_idx=idx,
                                               window_size=window_size)

                    sentiment = self._sentence_sentiment(text_chunk)

                    if sentiment['value'] == 'POSITIVE' and sentiment['confidence'] > self.exact_match_threshold:
                        return True
        return False

    def check_similarity(self, policy_text) -> float:
        """
        :param policy_text: checks how the text of policy is close to the GDPR requirements
        :return: similarity score
        """

        sim_checker = SimilarityChecker(self.language)
        similarity_score = sim_checker.check_query_doc(policy_text)
        return max(0, similarity_score)



    def analyse_text(self, policy_text: str) -> float:
        """
        main processing function
        :param policy_text: takes the text of the policy from the website
        :return: float from 0.0 (worst) to 1.0 (best) representing how good compiency is
        """

        policy_processed = preprocess_text(policy_text)

        # print("Evaluating Full overlaps")
        if self.check_exact_overlap(policy_processed, window_size=self.window_size):
            return 1.0

        # otherwise keep analyse all written points more in detail
        # which is a harder task
        res = self.check_similarity(policy_processed)
        return max(0, res)



if __name__ == "__main__":
    txt = """Everyone has the right to know what information about him is stored in different registers.
The right to inspect data, the exercise of the right to inspect and the rectification of data are regulated by the General EU Data Protection Regulation (2016/679).

Molok Oy's most important Personal Registers containing customer and partnership information and their data protection 
descriptions are broken down by personal register basis below. Other privacy statements concerning personal records will be provided separately upon request."""

    model = GDPR_Verifier(language="en", window_size=10)
    res = model.analyse_text(txt)

    print(f"Compliance of policy to GDPR: {res}")