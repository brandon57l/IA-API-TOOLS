from flask import Flask, request, jsonify, send_file
import requests

app = Flask(__name__)

# URL du serveur VoiceVox local
VOICEVOX_URL = "http://localhost:50021"

@app.route('/synthesize', methods=['GET'])
def synthesize_voice():
    # Récupérer les paramètres du GET
    text = request.args.get('text', "Hello world!")  # Valeur par défaut
    speaker = int(request.args.get('speaker', 1))  # Valeur par défaut
    # speedScale = float(request.args.get('speedScale', 1.0))  # Conversion en float
    # pitchScale = float(request.args.get('pitchScale', 1.0))
    intonationScale = float(request.args.get('intonationScale', 1.0))
    # volumeScale = float(request.args.get('volumeScale', 1.0))
    # prePhonemeLength = float(request.args.get('prePhonemeLength', 0.1))
    # postPhonemeLength = float(request.args.get('postPhonemeLength', 0.1))

    url = f"{VOICEVOX_URL}/audio_query?text={text}&speaker={speaker}"
    # Requête à VoiceVox pour générer l'audio_query en POST
    query_response = requests.post(url)
    
    if query_response.status_code != 200:
        # Détails de la requête (à ajuster selon votre besoin)
        request_details = request.json  # ou toute autre information que vous souhaitez afficher
        return jsonify({"error": "Failed to create audio query", "details": request_details}), 400
    

    audio_query = query_response.json()

    # Mettre à jour l'audio_query avec les autres paramètres
    audio_query.update({
        # "speedScale": speedScale,
        # "pitchScale": pitchScale,
        "intonationScale": intonationScale,
        # "volumeScale": volumeScale,
        # "prePhonemeLength": prePhonemeLength,
        # "postPhonemeLength": postPhonemeLength
    })

    # Requête à VoiceVox pour générer l'audio à partir de l'audio_query
    synthesis_response = requests.post(f"{VOICEVOX_URL}/synthesis?speaker={speaker}", json=audio_query)
    
    if synthesis_response.status_code != 200:
        return jsonify({"error": "Failed to synthesize audio"}), 500

    # Enregistrer le fichier audio temporairement
    audio_file = "output.wav"
    with open(audio_file, "wb") as f:
        f.write(synthesis_response.content)

    # Envoyer le fichier audio en réponse
    return send_file(audio_file, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
