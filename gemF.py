from flask import Flask, render_template, session, request
from gemML import extract_keywords_from_pdf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)
app.secret_key = 'ram110000'

@app.route('/')
def home():
    return render_template('gem.html')

@app.route('/summary1', methods=["GET", "POST"])
def summary1():
    top_10_keys = []
    if request.method == "POST":
        score = request.form['inputtext_'].strip()
        file_path = 'akbar.pdf' if score == 'akbar' else 'chandrayan3.pdf'
        raw_text, top_10_keys = extract_keywords_from_pdf(file_path)
        session['raw_text'] = raw_text
    return render_template('gem.html', summarized_text=top_10_keys)

@app.route('/summary2', methods=["GET", "POST"])
def summary2():
    if request.method == "POST":
        value = request.form['inputtext1_'].strip()
        raw_text = session.get('raw_text')
        print(raw_text)
    if raw_text is None:
        print("not found")
    similarity = calculate_similarity( value,raw_text)
    return f"Similarity between texts: {similarity}"

def calculate_similarity(value,raw_text):
    vectorizer = CountVectorizer().fit([value, raw_text])
    vector1, vector2 = vectorizer.transform([value, raw_text])
    cosine_sim = cosine_similarity(vector1, vector2)[0][0]
    print("Cosine similarity between the two texts:", cosine_sim)
    return cosine_sim

if __name__ == '__main__':
    app.run(debug=True)   


