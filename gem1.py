from flask import Flask, render_template,session,redirect,url_for,request
from PyPDF2 import PdfReader
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
stopwords= list(STOP_WORDS)
nlp=spacy.load('en_core_web_sm')
app = Flask(__name__)
app.secret_key='ram110000'
@app.route('/') 
def home():
    return render_template('gem.html')

@app.route('/summary1', methods=["GET","POST"])
def summary1():
    top_10_keys = []
    if request.method == "POST":
        score=request.form['inputtext_'].strip()
        if score=='akbar':
            pdfreader = PdfReader(r'akbar.pdf')
        else:
            pdfreader = PdfReader(r'chandrayan3.pdf')
        raw_text = ''
        for i, page in enumerate(pdfreader.pages):
            content = page.extract_text()
            if content:
                raw_text += content
                doc=nlp(raw_text)
                tokens=[token.text for token in doc]
#print(tokens)  ALL PUNCTUATION,STOPWORDS OIS INCLUDED HERE
                from string import punctuation
                punctuation=punctuation + '\n'
                word_frequencies={}
                for word in doc:
                    if word.text.lower() not in stopwords: #ELIMINATING STOPWORDS
                        if word.text.lower() not in punctuation:  #ELIMINATING PUNCTUATION
                            if word.text not in word_frequencies.keys():
                                word_frequencies[word.text] =1  #IF A WORD IS NEW, INCREASE FREQUENCY BY 1
                            else:
                                word_frequencies[word.text] += 1 #SAME WORDS, MORE THAN 1
                print('\n')
                max_value = max(word_frequencies.values())
                max_key = max(word_frequencies.keys())
                val = list(word_frequencies.values())  # Convert dict_values to a list
                val_sorted = sorted(val, reverse=True)  # Sort the list in descending order
                val_sorted=val_sorted[:7]
                dict={}
                sorted_items = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
                for word, frequency in sorted_items[:10]:
                    print(word, frequency)
                top_10_keys = [item[0] for item in sorted_items[:10]]
                for i in top_10_keys:
                    print(i, end="-")
                session['raw_text']=raw_text
    return render_template('gem.html', summarized_text=top_10_keys)

@app.route('/summary2',methods=["GET","POST"])
def summary2():
    if request.method == "POST":
        value=request.form['inputtext1_'].strip()
        raw_text=session.get('raw_text')
        print(value)
        print(raw_text)
        if raw_text is None:
            print("not found")
        else:
            vectorizer = CountVectorizer().fit([value, raw_text])
            vector1, vector2 = vectorizer.transform([value, raw_text])
# Calculate cosine similarity
            cosine_sim = cosine_similarity(vector1, vector2)[0][0]
    print("Cosine similarity between the two texts:", cosine_sim)
    return f"Similarity between texts: {cosine_sim}"

if __name__ == '__main__':
    app.run(debug=True)
