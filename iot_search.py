import nltk
from influxdb import InfluxDBClient
from baeza_yates_intersect import BaezaYates_intersect


class IotSearcher(object):
    def __init__(self, database='searcher', host="localhost", port=8086, user='root', password='root'):
        self._client = InfluxDBClient(host, port, user, password, database)
        self._client.drop_database(database)
        self._client.create_database(database)
        self._english_punctuations = set([',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '@', '#', '%', '$', '*'])
        self._stemmer = nltk.stem.lancaster.LancasterStemmer()
        self._stopwords = set(nltk.corpus.stopwords.words('english'))
        self._index_table = "iot_index"

    # def remove_index(self):
    #     self._client.drop_database(self._index_table)

    def _get_token(self, sentence):
        tokens = []
        for word in nltk.word_tokenize(sentence.lower()):
            if word not in self._english_punctuations and word not in self._stopwords:
                tokens.append(self._stemmer.stem(word))
        return tokens

    def index(self, doc_id, doc):
        values = {"doc_id": doc_id}
        for field, value in doc.iteritems():
            if type(value) in (int, long, float):
                values[field] = value

        rows_data = []
        for field, value in doc.iteritems():
            if type(value) is str:
                tokens = self._get_token(value)
                for token in tokens:
                    rows_data.append({
                            "measurement": self._index_table,
                            "tags": {"token": token, "field2": field},
                            "fields": values
                    })
        self._client.write_points(rows_data)

    def search(self, query, page=100):
        result = []
        field = None
        if "=" in query:
            field, query = query.split("=")
            query = query.replace("'", "")
            query = query.replace('"', "")
        words = self._get_token(query)
        for word in words:
            if field:
                response = self._client.query("select doc_id from %s WHERE token='%s' and field2='%s' ORDER BY time DESC LIMIT %d;" % (self._index_table, word, field, page))
            else:
                response = self._client.query("select doc_id from %s WHERE token='%s' ORDER BY time DESC LIMIT %d;" % (self._index_table, word, page))
            docs = [item["doc_id"] for r in response for item in r]
            if not result:
                result = docs
            else:
                result = BaezaYates_intersect(result, docs)
        print result
        return result


def main():
    searcher = IotSearcher()
    # searcher.remove_index()
    searcher.index(1, {"name": "bone lee", "age": 23, "cats": "ao da miao and ao er miao", "title": "this is a good title"})
    searcher.index(2, {"name": "jack lee", "age": 33, "cats": "unknown", "title": "hello world, this is from jack"})
    searcher.index(3, {"kaka": "how are you?"})
    searcher.search("lee")
    searcher.search("hello lee")
    searcher.search("this is a good miao")
    searcher.search("cats='da miao'")
    # TODO
    # searcher.search("cats='da miao' and name='bone'")

if __name__ == '__main__':
    main()

