import abc
import string

class SummaryCreatorBase(abc.ABC):
    # def __init__(self):
    #     pass

    def preprocess_text(self, text:str):
        punctuation = string.punctuation
        # we still want to keep some symbols like coma and full stop
        punctuation = punctuation.replace('.', '')
        punctuation = punctuation.replace(',', '')

        for s in punctuation:
            text = text.replace(s, '')

        # also delete unnecessary breaklines
        text = " ".join(text.split())

        return text



    @abc.abstractmethod
    def generate_summary(self, text: str):
        raise NotImplementedError

