import Classes.Path as Path
import pickle


# Efficiency and memory cost should be paid with extra attention.
#
# Please explain the code with necessary comments.
class MyIndexReader:
    def __init__(self, type):
        dir = Path.IndexTextDir if type == "trectext" else Path.IndexWebDir
        self.__dt_file = open(f"{dir}dict_term.pkl", "rb")
        self.__dt: dict[str, tuple[int, int]] = pickle.load(
            self.__dt_file
        )
        self.__hash_file = open(f"{dir}hash.pkl", "rb")
        self.__hash: list[str] = pickle.load(self.__hash_file)
        self.__posting = open(f"{dir}posting.txt", "r")
        print("finish reading the index")

    # Return the integer DocumentID of input string DocumentNo.
    def getDocId(self, docNo):
        return -1

    # Return the string DocumentNo of the input integer DocumentID.
    def getDocNo(self, docId: int):
        return self.__hash[docId]

    # Return DF.
    def DocFreq(self, token):
        _, pointer = self.__dt[token]
        self.__posting.seek(pointer)
        result = self.__posting.readline().strip().split(",")
        return len(result)

    # Return the frequency of the token in whole collection/corpus.
    def CollectionFreq(self, token):
        freq, _ = self.__dt[token]
        return freq

    # Return posting list in form of {documentID:frequency}.
    def getPostingList(self, token):
        _, pointer = self.__dt[token]
        self.__posting.seek(pointer)
        res = self.__posting.readline().strip().split(",")
        result={}
        for post in res:
            key, freq = post.split(":")
            result[int(key)] = freq
        return result
    
    def __del__(self):
        self.__dt_file.close()
        self.__hash_file.close()
        self.__posting.close()
