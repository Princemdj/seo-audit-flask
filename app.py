from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 SEO Audit API is running."

@app.route("/audit", methods=["POST"])
def audit():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"success": False, "error": "URL manquante"}), 400

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Exemple d’analyse simple
        title = soup.title.string if soup.title else "Aucun"
        description = soup.find("meta", attrs={"name": "description"})
        description = description["content"] if description else "Aucune"
        h1 = soup.find("h1").text if soup.find("h1") else "Aucun"

        audit_result = {
            "url": url,
            "title": title,
            "description": description,
            "h1": h1
        }

        return jsonify({"success": True, "data": audit_result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
