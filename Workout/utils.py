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

# def predict_performance(user):
#     past_progress = Progress.objects.filter(user=user, is_done=True)

#     if not past_progress:
#         return {"average_duration": 0, "average_repetitions": 0}

#     durations = [progress.workout.exercises.first().duration for progress in past_progress if progress.workout.exercises.exists()]
#     repetitions = [progress.workout.exercises.first().repetitions for progress in past_progress if progress.workout.exercises.exists()]

#     if not durations or not repetitions:
#         return {"average_duration": 0, "average_repetitions": 0}

#     X = np.array(durations).reshape(-1, 1)
#     y = np.array(repetitions)

#     model = LinearRegression()
#     model.fit(X, y)

#     predicted_repetitions = model.predict(X).mean()

#     return {
#         "average_duration": np.mean(durations),
#         "average_repetitions": predicted_repetitions,
#     }



# import pandas as pd
# from .models import Progress,WorkoutExercise
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression

# # def get_user_progress_data(user):
# #     # Récupérer les données de progrès pour un utilisateur donné
# #     progress_data = Progress.objects.filter(user=user)
# #     data = {
# #         'date_completed': [],
# #         'duration': [],
# #         'repetitions': [],
# #         'weight': [],
# #         'is_done': []
# #     }

# #     for progress in progress_data:
# #         data['date_completed'].append(progress.date_completed)
# #         data['duration'].append(progress.duration.total_seconds() if progress.duration else 0)
# #         data['repetitions'].append(progress.repetitions or 0)
# #         data['weight'].append(progress.weight or 0)
# #         data['is_done'].append(progress.is_done)

# #     return pd.DataFrame(data)


# # def train_model(user):
# #     df = get_user_progress_data(user)
# #     X = df[['duration', 'repetitions', 'weight']]
# #     y = df['is_done']  # Ou toute autre métrique que vous voulez prédire

# #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# #     model = LinearRegression()
# #     model.fit(X_train, y_train)

# #     return model

# # def predict_performance(user, new_data):
# #     model = train_model(user)
# #     prediction = model.predict([new_data])  # new_data = [duration, repetitions, weight]
# #     return prediction

# def predict_performance(user):
#     # Récupérer les progrès passés pour l'utilisateur
#     past_progress = Progress.objects.filter(user=user)

#     # Si pas de progrès, retourner None
#     if not past_progress:
#         return {"average_duration": 0, "average_repetitions": 0}

#     total_duration = 0
#     total_repetitions = 0
#     count = 0

#     for progress in past_progress:
#         workout_exercises = WorkoutExercise.objects.filter(workout=progress.workout)
#         duration = sum(exercise.exercise.duration for exercise in workout_exercises if exercise.exercise.duration)
#         repetitions = sum(exercise.repetitions for exercise in workout_exercises)

#         total_duration += duration
#         total_repetitions += repetitions
#         count += 1

#     return {
#         "average_duration": total_duration / count if count > 0 else 0,
#         "average_repetitions": total_repetitions / count if count > 0 else 0,
#     }
