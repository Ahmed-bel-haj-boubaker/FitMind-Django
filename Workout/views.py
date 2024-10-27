from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Exercise, Workout, WorkoutExercise, Progress
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.conf import settings
from .forms import WorkoutRecommendationForm,WorkoutForm,ExerciseForm, ExerciseForm
import random
import requests
import os
from django.views.generic import ListView,TemplateView
from django.forms import formset_factory
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .utils import predict_performance
from random import randint
from django.utils.html import format_html
import replicate
from django.http import JsonResponse
import random
from django.db.models import Count
from django.core.paginator import Paginator
from .recommendation import recommend_workouts

# Create your views here.
class WorkoutListView(ListView):
    model = Workout
    template_name = 'workout_list.html'
    context_object_name = 'workouts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all workouts created by other users
        context['other_user_workouts'] = Workout.objects.exclude(created_by=self.request.user)

        # Get workouts created by the logged-in user
        context['my_workouts'] = Workout.objects.filter(created_by=self.request.user)

        return context
    
class WorkoutDetailView(DetailView):
    model = Workout
    template_name = 'workout_detail.html'
    context_object_name = 'workout'
    def get_context_data(self, **kwargs):
        # Obtenir le contexte de base (le workout)
        context = super().get_context_data(**kwargs)
        
        # Récupérer les catégories d'exercices et le nombre d'exercices par catégorie
        categories = Exercise.objects.values('category').annotate(exercise_count=Count('category'))
        
        # Ajouter les catégories au contexte pour les utiliser dans le template
        context['categories'] = categories
        
        return context

class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    form_class = WorkoutForm  # Utilisez le formulaire personnalisé
    template_name = 'workout_form.html'
    success_url = reverse_lazy('workout_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    model = Workout
    form_class = WorkoutForm  
    template_name = 'workout_form.html'
    success_url = reverse_lazy('workout_list')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    model = Workout
    template_name = 'workout_confirm_delete.html'
    success_url = reverse_lazy('workout_list')


def generate_suggestion(text):
    if text:
        input_data = {
            "prompt": f"Complete the following sentence. Don't write more than 1 sentence.\n----\n{text}",
            "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
                              "You are a helpful assistant. Don't include the start of the sentence. "
                              "Only include your completion. "
                              "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}"
                              "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
            "presence_penalty": 0,
            "frequency_penalty": 0
        }

        output = replicate.run("meta/meta-llama-3-8b-instruct", input=input_data)
        completion = "".join(output)
        return completion.strip()
    
    return ""

 
def analyze_nutrition(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire (par exemple, la recette en texte)
        recipe_text = request.POST.get('recipe')

        # Préparer la requête pour l'API Edamam
        url = "https://api.edamam.com/api/nutrition-details"
        app_id = '092a002a'
        app_key = 'a997206f10d9315f62f8eb99ec564bb7'
        
        recipe_data = {
            "title": "User's Recipe",
            "ingr": recipe_text.splitlines()  # Diviser le texte en lignes
        }

        # Envoyer la requête POST à l'API
        response = requests.post(url, json=recipe_data, params={'app_id': app_id, 'app_key': app_key})

        if response.status_code == 200:
            nutrition_data = response.json()
            return render(request, 'nutrition_results.html', {'nutrition_data': nutrition_data})
        else:
            error_message = f"Erreur lors de l'analyse nutritionnelle: {response.status_code}"
            return render(request, 'nutrition_form.html', {'error': error_message})
    else:
        return render(request, 'nutrition_form.html')
    
    
def recommend_workout(request):
    if request.method == 'POST':
        form = WorkoutRecommendationForm(request.POST)
        if form.is_valid():
            workout_type = form.cleaned_data['workout_type']
            level = form.cleaned_data['level']
            
            # Filtrer les workouts disponibles en fonction des préférences
            recommended_workouts = Workout.objects.filter(level=level)
            
            # Filtrer les workouts par type si c'est nécessaire
            if workout_type:
                recommended_workouts = recommended_workouts.filter(exercises__category=workout_type)
            
            # Sélectionner un workout aléatoirement parmi les correspondances
            if recommended_workouts.exists():
                workout = random.choice(recommended_workouts)
            else:
                workout = None
            
            return render(request, 'workout_recommendation.html', {
                'workout': workout,
                'form': form,
            })
    else:
        form = WorkoutRecommendationForm()
    
    return render(request, 'workout_recommendation.html', {'form': form})
def create_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST,request.FILES)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.save()
            return redirect('workout_create')  # Rediriger vers la liste des exercices ou une autre page
    else:
        form = ExerciseForm()

    return render(request, 'create_exercise.html', {'form': form})

@login_required
def add_to_todo_list(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    progress, created = Progress.objects.get_or_create(user=request.user, workout=workout)
    
    if created:
        return redirect('todo_list')
    else:
        # Si le workout est déjà dans la liste
        return render(request, 'workout_already_added.html')

@login_required
def mark_as_done(request, progress_id):
    progress = Progress.objects.get(id=progress_id)
    progress.is_done = True
    progress.date_completed = timezone.now()
    progress.progress_percentage = 100.0  # Workout complété à 100%
    progress.save()
    
    return redirect('todo_list')

@login_required
def todo_list(request):
    todo_workouts = Progress.objects.filter(user=request.user, is_done=False)
    done_workouts = Progress.objects.filter(user=request.user, is_done=True)
    
    return render(request, 'todo_list.html', {
        'todo_workouts': todo_workouts,
        'done_workouts': done_workouts
    })
# @login_required
# def dashboard(request):
#     # Utiliser l'IA pour prédire la performance
#     predicted_performance = predict_performance(request.user)

#     # Récupérer les progrès passés
#     past_progress = Progress.objects.filter(user=request.user)

#     return render(request, 'dashboard.html', {
#         'predicted_performance': predicted_performance,
#         'past_progress': past_progress,
#     })
  
@login_required
def dashboard(request):
    # Utiliser l'IA pour prédire la performance
    performance_data = predict_performance(request.user)

    # Récupérer les progrès passés
    past_progress = Progress.objects.filter(user=request.user)

    # Obtenir les recommandations de workout basées sur l'IA
    recommended_workouts = recommend_workouts(request.user.id)

    return render(request, 'dashboard.html', {
        'predicted_performance': performance_data['predicted_progress'],
        'progress_percentage': performance_data['progress_percentage'],  # Pourcentage de progression
        'expected_progress': performance_data['expected_progress'],  # Pourcentage de progression attendu
        'past_progress': past_progress,
        'recommended_workouts': recommended_workouts,
    })

    
class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    

   
API_URL = 'https://api.edamam.com/api/recipes/v2'
APP_ID = 'd8d480c2' 
API_KEY = '5553fd43abafa71ba2f18dbca8ce0d92'  

def search_food(request):
    results = []
    if request.method == 'POST':
        keywords = request.POST.get('keywords')
        response = requests.get(API_URL, params={'keywords': keywords}, auth=(APP_ID, API_KEY))
        if response.status_code == 200:
            results = response.json().get('results', [])
    
    return render(request, 'search.html', {'results': results})

def exercise_list(request):
    query = request.GET.get('search', '')
    exercises = Exercise.objects.filter(name__icontains=query)

    # Pagination
    paginator = Paginator(exercises, 5)  # 10 exercices par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Organiser par catégorie
    categories = {category: exercises.filter(category=category) for category in Exercise.objects.values_list('category', flat=True).distinct()}

    return render(request, 'exercise_list.html', {'page_obj': page_obj, 'categories': categories, 'query': query})

def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    return render(request, 'exercise_detail.html', {'exercise': exercise})
