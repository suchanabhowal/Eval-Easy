import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from PyPDF2 import PdfReader
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')

import google.generativeai as genai
import os
import re
os.environ['GOOGLE_API_KEY']="####"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

def extract_keywords_from_pdf(content):
    raw_text = ''
    raw_text = content
    raw_text = re.sub(r'\n{2,}', ' ', raw_text)
    # Remove special characters except alphabets, digits, and whitespaces
    raw_text= re.sub(r'[^\w\s]', '', raw_text)
    # Remove leading and trailing whitespaces
    raw_text = raw_text.strip()
    print("GEMINI PARA AFTER REGULAR PREPROCESS")
    doc = nlp(raw_text)   
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1
    sorted_items = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
    top_10_keys = [item[0] for item in sorted_items[1:12]]
    
    return raw_text, top_10_keys


def calculate_similarity(value,raw_text):
    vectorizer = CountVectorizer().fit([value, raw_text])
    vector1, vector2 = vectorizer.transform([value, raw_text])
    cosine_sim = cosine_similarity(vector1, vector2)[0][0]
    print("Cosine similarity between the two texts:", cosine_sim)
    cosine_sim= .1 * cosine_sim
    return cosine_sim

def total_similarity(value,raw_text,top_10_keys):
    vectorizer = CountVectorizer().fit([value, raw_text])
    vector1, vector2 = vectorizer.transform([value, raw_text])
    cosine_sim = cosine_similarity(vector1, vector2)[0][0]
    print("Cosine similarity between the two texts:", cosine_sim)
    cosine_sim= .1 * cosine_sim

#value is student report
#raw_text is gemini text
    matches = 0
    grade=0
    text_lower = value.lower()
    keywords_lower = [keyword.lower() for keyword in top_10_keys]
    for keyword in keywords_lower:
    # Check if the keyword is present in the text
        if keyword in text_lower:
            matches += 1
    if matches == 10:
        grade = 100
    elif matches >= 5 and matches< 10:
        grade = 50
    elif matches < 5:
        grade = 20
    grade = .5 * grade
    print(f"The text contains {matches} out of {len(top_10_keys)} keywords.")
    print(f"Grade: {grade}") 

    total_sim = grade + cosine_sim
    return total_sim 





def get_gemini_response(score):
    response=model.generate_content(score)
    return response.text

