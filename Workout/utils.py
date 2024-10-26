import numpy as np
from sklearn.linear_model import LinearRegression
from .models import Progress
import joblib


# def predict_performance(user):
#     # Charger le modèle
#     model = joblib.load('performance_model.pkl')

#     # Récupérer les progrès passés pour l'utilisateur
#     past_progress = Progress.objects.filter(user=user)

#     if not past_progress:
#         return {"predicted_progress": 0}

#     # Préparer les données pour la prédiction
#     durations = [progress.workout.exercises.first().duration for progress in past_progress if progress.workout.exercises.first().duration]
#     repetitions = [progress.workout.exercises.first().repetitions for progress in past_progress if progress.workout.exercises.first().repetitions]

#     # Calculer la moyenne des durées et des répétitions
#     avg_duration = np.mean(durations)
#     avg_repetitions = np.mean(repetitions)

#     # Faire la prédiction
#     predicted_progress = model.predict(np.array([[avg_duration, avg_repetitions]]))[0]

#     return {"predicted_progress": predicted_progress}



def predict_performance(user):
    # Charger le modèle
    model = joblib.load('performance_model.pkl')

    # Récupérer les progrès passés pour l'utilisateur
    past_progress = Progress.objects.filter(user=user)

    # Si aucun progrès n'est trouvé
    if not past_progress:
        return {"predicted_progress": 0, "progress_percentage": 0, "expected_progress": 0}

    # Compter le nombre total de workouts et de workouts complétés
    total_workouts = 5  # Supposons que nous voulons une base de 5 workouts pour 100%
    completed_workouts = past_progress.filter(is_done=True).count()

    # Calculer le pourcentage de progression
    progress_percentage = (completed_workouts / total_workouts) * 100

    # Préparer les données pour la prédiction
    durations = [progress.workout.exercises.first().duration for progress in past_progress if progress.workout.exercises.first().duration]
    repetitions = [progress.workout.exercises.first().repetitions for progress in past_progress if progress.workout.exercises.first().repetitions]

    # Calculer la moyenne des durées et des répétitions
    avg_duration = np.mean(durations) if durations else 0
    avg_repetitions = np.mean(repetitions) if repetitions else 0

    # Faire la prédiction basée sur les données moyennes
    predicted_progress = model.predict(np.array([[avg_duration, avg_repetitions]]))[0]

    # Calculer l'expected progress en fonction du nombre de workouts effectués
    expected_progress = (completed_workouts / total_workouts) * 100

    # Assurez-vous que predicted_progress ne soit pas inférieur à 0
    predicted_progress = max(predicted_progress, 0)

    # Ajuster predicted_progress pour être au moins égal à expected_progress + 10
    predicted_progress = max(predicted_progress, expected_progress + 10)

    # Assurez-vous que le predicted_progress ne dépasse pas 100%
    if predicted_progress > 100:
        predicted_progress = 100

    return {
        "predicted_progress": predicted_progress,
        "progress_percentage": progress_percentage,
        "expected_progress": expected_progress,
    }