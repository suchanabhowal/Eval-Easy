import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from PyPDF2 import PdfReader
from string import punctuation
stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')


def extract_keywords_from_pdf(file_path):
    pdfreader = PdfReader(file_path)
    raw_text = ''
    for i, page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            raw_text += content
    doc = nlp(raw_text)
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1
    sorted_items = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
    top_10_keys = [item[0] for item in sorted_items[:10]]
    return raw_text, top_10_keys
