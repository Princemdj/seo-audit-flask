from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # autorise les requêtes depuis ton site WordPress

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json
    prenom = data.get('prenom')
    email = data.get('email')
    url = data.get('url')

    if not prenom or not email or not url:
        return jsonify({'success': False, 'message': 'Champs requis manquants'}), 400

    # Simuler un audit de base (tu pourras le remplacer par l'audit réel)
    result = {
        'titre': 'Titre Exemple',
        'meta': 'Meta description exemple',
        'h1': 'Titre principal (H1)',
        'mots': 350,
        'images': 6,
        'images_sans_alt': 2
    }

    return jsonify({'success': True, 'data': result})

if __name__ == '__main__':
    app.run(debug=True)
