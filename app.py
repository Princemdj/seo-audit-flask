from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 SEO Audit API is running."

@app.route("/audit", methods=["GET"])
def audit():
    data = request.get_json()
    url = data.get("url")
    
    if not url:
        return jsonify(success=False, error="URL manquante")

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "Aucun titre"
        description = soup.find("meta", attrs={"name": "description"})
        description = description["content"].strip() if description else "Aucune meta description"
        h1 = soup.find("h1")
        h1 = h1.get_text(strip=True) if h1 else "Aucune balise H1"

        return jsonify(success=True, data={
            "title": title,
            "description": description,
            "h1": h1
        })

    except Exception as e:
        return jsonify(success=False, error=str(e))

# ✅ Partie importante pour Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
