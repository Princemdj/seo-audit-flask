from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Autoriser les appels cross-origin (nécessaire pour WordPress)

@app.route('/api/audit', methods=['GET'])
def audit():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else ''
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        meta_desc = meta_desc_tag['content'] if meta_desc_tag else ''
        h1_tag = soup.find('h1')
        h1 = h1_tag.text.strip() if h1_tag else ''
        canonical = soup.find('link', rel='canonical')
        canonical_url = canonical['href'] if canonical else ''
        robots_meta = soup.find('meta', attrs={'name': 'robots'})
        robots_content = robots_meta['content'] if robots_meta else ''

        words = len(soup.get_text().split())
        images = soup.find_all('img')
        total_images = len(images)
        images_without_alt = len([img for img in images if not img.get('alt')])

        return jsonify({
            'title': title,
            'meta_description': meta_desc,
            'h1': h1,
            'canonical': canonical_url,
            'robots': robots_content,
            'word_count': words,
            'image_count': total_images,
            'images_missing_alt': images_without_alt
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return 'SEO Audit API is running'

# ✅ Ajout crucial pour Render : écouter le bon port dynamiquement
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
