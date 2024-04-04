from flask import Flask, render_template, session, request
from gemML1 import get_gemini_response,extract_keywords_from_pdf,total_similarity,calculate_similarity

app = Flask(__name__)
app.secret_key = 'ram110000'

@app.route('/')
def home():
    return render_template('gem1.html')

@app.route('/summary1', methods=["GET", "POST"])
def summary1():
    top_10_keys = []
    if request.method == "POST":
        score = request.form['inputtext_'].strip()
        file_path = get_gemini_response(score)
        raw_text, top_10_keys = extract_keywords_from_pdf(file_path)
        session['raw_text'] = raw_text
        session['top_10_keys'] = top_10_keys
    return render_template('gem1.html', summarized_text=top_10_keys)

@app.route('/summary2', methods=["GET", "POST"])
def summary2():
    if request.method == "POST":
        value = request.form['inputtext1_'].strip()
        raw_text = session.get('raw_text')
        top_10_keys = session.get('top_10_keys')
        print("GEMINI RESPONSE STORED AS RAW_TEXT INSIDE TH EFLASK FILE\n\n\n")
        print(raw_text)
    if raw_text is None:
        print("not found")
    similarity=total_similarity(value,raw_text,top_10_keys)
    #similarity=calculate_similarity(value,raw_text)
    #total_similarity()
    return f"Similarity between texts: {similarity}"


if __name__ == '__main__':
    app.run(debug=True)   


