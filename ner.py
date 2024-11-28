import datetime
import json
from flair.data import Sentence
from flair.models import SequenceTagger

# load tagger
tagger = SequenceTagger.load("flair/ner-german")

def preprocess_data(data):
    if isinstance(data, dict):
        return {k: preprocess_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [preprocess_data(v) for v in data]
    elif isinstance(data, set):
        return list(data)  # Convert set to list
    elif isinstance(data, (datetime.date, datetime.datetime)):
        return data.isoformat()  # Convert datetime to ISO format string
    elif isinstance(data, tuple):
        return list(data)  # Convert tuple to list
    else:
        return data

def analyze_text(snippet):

    if not snippet:
        snippet = "Lars Walther, educorvi GmbH & Co.KG, Karolinenstraße 17, 90763 Fürth"

    sentence = Sentence(snippet)

    # predict NER tags
    tagger.predict(sentence)

    # print predicted NER spans
    print('The following NER tags are found:')
    # iterate over entities and print
    print(sentence.get_spans('ner'))
    test = sentence.get_spans('ner')
    print("----" * 10)
    nerlist = []
    for entity in sentence.get_spans('ner'):
        mydict = {}
        mydict["entity"] = f"{preprocess_data(entity)}"
        mydict["text"] = preprocess_data(entity.text)
        mydict["tag"] = preprocess_data(entity.tag)
        mydict["score"] = preprocess_data(entity.score)
        mydict["start"] = preprocess_data(entity.start_position)
        mydict["end"] = preprocess_data(entity.end_position)
        nerlist.append(mydict)
    json_string = json.dumps(nerlist)
    print('JSON')
    print(json_string)
    return json_string
