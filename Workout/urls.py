from django.urls import path
from .views import exercise_detail,exercise_list,search_food,WorkoutListView, WorkoutDetailView, WorkoutCreateView, WorkoutUpdateView, WorkoutDeleteView,create_exercise,DashboardView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import dashboard


urlpatterns = [
    path('workouts/', WorkoutListView.as_view(), name='workout_list'),
    path('workouts/<int:pk>/', WorkoutDetailView.as_view(), name='workout_detail'),
    path('workouts/create/', WorkoutCreateView.as_view(), name='workout_create'),
    path('workouts/<int:pk>/update/', WorkoutUpdateView.as_view(), name='workout_update'),
    path('workouts/<int:pk>/delete/', WorkoutDeleteView.as_view(), name='workout_delete'),
    path('analyze-nutrition/', views.analyze_nutrition, name='analyze_nutrition'),
    path('recommend-workout/', views.recommend_workout, name='recommend_workout'),
    path('exercises/create/', create_exercise, name='create_exercise'),
    path('add-to-todo/<int:workout_id>/', views.add_to_todo_list, name='add_to_todo'),
    path('mark-as-done/<int:progress_id>/', views.mark_as_done, name='mark_as_done'),
    path('todo-list/', views.todo_list, name='todo_list'),
   # path('dashboard/', DashboardView.as_view(), name='dashboard'), 
    path('search/', search_food, name='search'),
    path('exercises/', exercise_list, name='exercise_list'),
    path('exercises/<int:exercise_id>/', exercise_detail, name='exercise_detail'),  # Ajoutez cette ligne
    path('dashboard/', dashboard, name='dashboard'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
