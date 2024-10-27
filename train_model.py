import os
import django

# Définir le module de paramètres de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitmind.settings') 

# Initialiser Django
django.setup()

from Workout.models import Progress
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

def train_performance_model():
    # Récupérer les données des progrès
    progress_data = Progress.objects.all()

    # Créer un DataFrame
    data = {
        'duration': [],
        'repetitions': [],
        'progress_percentage': []
    }

    for progress in progress_data:
        workout = progress.workout
        # Assurez-vous que chaque workout a au moins un exercice
        if workout.exercises.exists():
            data['duration'].append(workout.exercises.first().duration)  # Prendre le premier exercice pour l'exemple
            data['repetitions'].append(workout.exercises.first().repetitions)
            data['progress_percentage'].append(progress.progress_percentage)

    df = pd.DataFrame(data)

    # Supprimer les lignes avec des valeurs manquantes
    df.dropna(inplace=True)

    # Vérifiez si nous avons suffisamment de données
    if df.shape[0] < 2:  # Moins de 2 échantillons
        print("Pas assez de données pour entraîner le modèle.")
        return

    # Séparer les caractéristiques et la cible
    X = df[['duration', 'repetitions']]
    y = df['progress_percentage']

    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Créer et entraîner le modèle
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Enregistrer le modèle
    joblib.dump(model, 'performance_model.pkl')

    print("Modèle d'IA entraîné et enregistré avec succès.")

if __name__ == '__main__':
    train_performance_model()
