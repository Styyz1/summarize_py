from flask import Flask, render_template, request
from summarize import summarize_text  # Importe ta fonction de résumé

app = Flask(__name__)

# Page d'accueil avec le formulaire de soumission
@app.route('/')
def index():
    return render_template('index.html')

# Route pour traiter le texte soumis et afficher le résumé
@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        text = request.form['text']  # Récupère le texte entré
        lang = request.form['lang']  # Récupère la langue choisie
        num_sentences = int(request.form['num_sentences'])  # Nombre de phrases dans le résumé

        # Appelle la fonction de résumé
        summary = summarize_text(text, lang=lang, num_sentences=num_sentences)

        # Renvoie le résumé à la page
        return render_template('index.html', summary=summary, original=text, lang=lang)

if __name__ == '__main__':
    app.run(debug=True)