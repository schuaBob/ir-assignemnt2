import Classes.Path as Path

# Please explain the code with necessary comments.
class PreprocessedCorpusReader:

    def __init__(self, type):
        self.file = open(f"{Path.ResultHM1}{type}", "r")

    # Read a line for docNo from the corpus, read another line for the content, and return them in [docNo, content].
    def nextDocument(self):
        docNo = self.file.readline().strip()
        content = self.file.readline().strip()
        return [docNo, content]
    
    def __del__(self):
        self.file.close()