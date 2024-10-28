import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer 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"}

def generate_summary(text):
    if not text.strip():  # Vérifie si le texte est vide
        return "Erreur : Le texte est vide, impossible de générer un résumé."

    payload = {"inputs": text}
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Lever une exception en cas d'erreur HTTP

        # Afficher la réponse complète pour le débogage
        print("Réponse complète de l'API : ", response.json())

        result = response.json()

        # Vérifier la structure de la réponse pour trouver le résumé
        if isinstance(result, list) and 'summary_text' in result[0]:
            return result[0]['summary_text']
        else:
            return f"Erreur : Résumé non trouvé dans la réponse - {result}"
    except requests.exceptions.HTTPError as http_err:
        return f"Erreur API : {http_err}"
    except Exception as err:
        return f"Erreur : {err}"


def clean_summary(summary, original):
    """Évite les paraphrases et doublons dans le résumé."""
    # Supprime le texte d'origine s'il est présent dans le résumé
    if original.strip() in summary.strip():
        return summary.replace(original, "").strip()
    return summary