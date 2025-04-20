from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import uuid
app = Flask(__name__)
CORS(app)  # <-- Ajout ici pour autoriser toutes les origines





@app.route('/payer', methods=['POST'])
def payer():
    try:
        data = request.get_json()
        nom = data.get('nom')
        montant = data.get('montant')
        # article_id = data.get('id')
        description = data.get('description')
        try:
            montant = int(montant)
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'message': 'Le montant doit être un entier valide.'
    }), 400

        if not nom or not montant:
            return jsonify({
                'status': 'error',
                'message': 'Nom et montant sont requis.'
            }), 400

        order_id = str(uuid.uuid4())

        payload = {
            "amount": montant,
            "shop_name": nom,
            "message":   f"{description}",
            "success_url": "https://tonsite.com/success",
            "failure_url": "https://tonsite.com/failure",
            "order_id":    order_id 
        }
        headers = {
            "api-key": "lygosapp-43b002d7-b622-4107-9e8d-319c2275e39f",
            "Content-Type": "application/json"
        }

        response = requests.post("https://api.lygosapp.com/v1/gateway", json=payload, headers=headers)
        response.raise_for_status()  # Provoque une erreur si la réponse est mauvaise

        data = response.json()
        lien_paiement = data.get("link")

        return jsonify({
            'status': 'success',
            'message': f'Paiement de {montant} CDF initié pour {nom}',
            'payment_link': lien_paiement
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Erreur interne',
            'details': str(e)
        }), 500
if __name__ == '__main__':
    app.run(debug=True)
    
