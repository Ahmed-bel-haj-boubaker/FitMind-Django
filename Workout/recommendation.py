import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from Workout.models import Progress, Workout

def get_user_workout_matrix():
    # Collecter les données de progression des utilisateurs
    progress_data = Progress.objects.filter(is_done=True)
    
    # Créer un DataFrame contenant les utilisateurs et les workouts complétés
    data = []
    for progress in progress_data:
        data.append({
            'user_id': progress.user.id,
            'workout_id': progress.workout.id,
            'progress_percentage': progress.progress_percentage
        })
    
    df = pd.DataFrame(data)
    
    # Créer une matrice utilisateur-workout
    user_workout_matrix = df.pivot_table(index='user_id', columns='workout_id', values='progress_percentage', fill_value=0)
    
    return user_workout_matrix

def recommend_workouts(user_id, top_n=5):
    # Obtenir la matrice utilisateur-workout
    user_workout_matrix = get_user_workout_matrix()
    
    # Calculer la similarité entre les utilisateurs
    similarity_matrix = cosine_similarity(user_workout_matrix)
    
    # Obtenir l'index de l'utilisateur actuel
    user_idx = list(user_workout_matrix.index).index(user_id)
    
    # Obtenir les similarités pour l'utilisateur actuel
    user_similarities = similarity_matrix[user_idx]
    
    # Trier les utilisateurs similaires par score de similarité
    similar_users = sorted(list(enumerate(user_similarities)), key=lambda x: x[1], reverse=True)
    
    # Récupérer les workouts recommandés des utilisateurs similaires
    recommended_workouts = []
    for similar_user in similar_users[1:]:
        similar_user_id = user_workout_matrix.index[similar_user[0]]
        similar_user_workouts = user_workout_matrix.loc[similar_user_id]
        
        # Filtrer les workouts non encore complétés par l'utilisateur actuel
        for workout_id, progress in similar_user_workouts.items():
            if progress > 0 and user_workout_matrix.loc[user_id, workout_id] == 0:
                recommended_workouts.append(workout_id)
        
        if len(recommended_workouts) >= top_n:
            break
    
    # Limiter à 'top_n' workouts recommandés
    recommended_workouts = recommended_workouts[:top_n]
    
    return Workout.objects.filter(id__in=recommended_workouts)
