import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image

# Charger le modèle MoveNet
movenet = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4").signatures['serving_default']

def estimate_pose(image_path):
    # Charger l'image et la prétraiter
    try:
        image = Image.open(image_path).convert('RGB')  # Assurer que l'image est en RGB
        image = image.resize((192, 192))  # Redimensionner à 192x192
        image_np = np.array(image).astype(np.int32) / 255.0  # Normaliser l'image

        # Ajouter une dimension de lot
        input_image = np.expand_dims(image_np, axis=0)

        # Exécuter le modèle
        outputs = movenet(tf.convert_to_tensor(input_image, dtype=tf.int32))
        keypoints = outputs['output_0'].numpy()  # Extraire les points clés

        # Vérifier et retourner les points clés
        if keypoints is not None:
            return keypoints[0][0]  # Retourner les points clés pour la première personne détectée
        else:
            return None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None