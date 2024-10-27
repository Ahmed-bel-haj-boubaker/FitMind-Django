import numpy as np
from sklearn.linear_model import LinearRegression
from .models import Progress
import joblib


def predict_performance(user):
    # Charger le modèle
    model = joblib.load('performance_model.pkl')

    # Récupérer les progrès passés pour l'utilisateur
    past_progress = Progress.objects.filter(user=user)

    if not past_progress:
        return {"predicted_progress": 0}

    # Préparer les données pour la prédiction
    durations = [progress.workout.exercises.first().duration for progress in past_progress if progress.workout.exercises.first().duration]
    repetitions = [progress.workout.exercises.first().repetitions for progress in past_progress if progress.workout.exercises.first().repetitions]

    # Calculer la moyenne des durées et des répétitions
    avg_duration = np.mean(durations)
    avg_repetitions = np.mean(repetitions)

    # Faire la prédiction
    predicted_progress = model.predict(np.array([[avg_duration, avg_repetitions]]))[0]

    return {"predicted_progress": predicted_progress}
