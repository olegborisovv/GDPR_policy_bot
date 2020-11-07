from Web_Application.SummaryCreator.SummaryCreatorBase import SummaryCreatorBase
# from summarizer import Summarizer


class DeepLearningSummarizer(SummaryCreatorBase):
    # def __init__(self):
    #     pass

    def generate_summary(self, text: str):

        text = self.preprocess_text(text)

        # this ML system is limited to 1 000 000 character only therefroe it is important to cut the text as well
        text = text[:999999]

        # model = Summarizer()
        #
        # result = model(text, min_length=10, max_length=50)
        result = "Currently old module is not supported"
        full = ''.join(result)

        return full