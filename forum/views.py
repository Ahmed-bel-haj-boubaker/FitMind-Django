from django.shortcuts import render, get_object_or_404, redirect
from .models import Sujet ,ReplaySujet,Reaction
from .form import SujetForm
from .formEdit import postForm 
from .formReplay import ReplayForm 

from django.contrib.auth.decorators import login_required  
from django.http import JsonResponse

from .utils import analyse_sentiment_emoji  # Importer la fonction d'analyse
from .resume import generate_summary,clean_summary  # Importer la fonction


# Create your views here.

def index(request):
    sujets=Sujet.objects.all()

    return render(request, "ListeSujet.html" , {'sujets': sujets})

@login_required
def addSujet(request):
    if request.method == 'POST':
        form = SujetForm(request.POST, request.FILES)
        if form.is_valid():
            sujet = form.save(commit=False) 
            sujet.user = request.user  
            sujet.statut = 'non_resolu' 
            sujet.save() 
            return redirect('forum_home')
    else:
        form = SujetForm()
    return render(request, 'addSujet.html', {'form': form})

@login_required
def editSujet(request, pk):
    sujet = get_object_or_404(Sujet, pk=pk)
    if sujet.user != request.user:
        return redirect('forum_home')  
    if request.method == 'POST':
        form = postForm(request.POST, request.FILES, instance=sujet)
        if form.is_valid():
            form.save()
            return redirect('forum_home') 
    else:
        form = postForm(instance=sujet)

    return render(request, "editSujet.html" , {'form': form, 'sujet': sujet})

def indexReplay(request, pk):
    """Affiche les détails du sujet avec traduction et gère les replays."""
    sujet = get_object_or_404(Sujet, pk=pk)

    # Générer le résumé et le nettoyer
    summary = generate_summary(sujet.description)
    summary = clean_summary(summary, sujet.description)

    like_count = Reaction.objects.filter(sujet=sujet, reaction='like').count()
    dislike_count = Reaction.objects.filter(sujet=sujet, reaction='dislike').count()

    # Récupérer les replays associés au sujet
    replays = ReplaySujet.objects.filter(sujet=sujet).order_by('-date_creation')

    # Ajouter un sentiment avec emoji et une traduction à chaque replay
    for replay in replays:
        replay.sentiment_emoji = analyse_sentiment_emoji(replay.message)
    

    # Gérer l'ajout de nouveaux replays
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            ReplaySujet.objects.create(
                message=message,
                sujet=sujet,
                user=request.user
            )
            return redirect('forum_replay', pk=sujet.pk)

    # Rendre le template avec les données
    return render(request, 'ListeReplay.html', {
        'sujet': sujet,
        'replays': replays,
        'summary': summary,
        'like_count':like_count,
        'dislike_count':dislike_count,
    })
@login_required
def sujet_delete(request, pk):
    # Récupérer le sujet par son ID
    sujet = get_object_or_404(Sujet, pk=pk)

    # Vérification : L'utilisateur connecté est le créateur du sujet
    if sujet.user != request.user:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    # Supprimer le sujet
    sujet.delete()

    # Retourner une réponse JSON pour indiquer que la suppression a été effectuée
    return redirect('forum_home')



@login_required
def replay_delete(request, pk):
    
    replay = get_object_or_404(ReplaySujet, pk=pk)

    # Vérifier si l'utilisateur connecté est bien l'auteur du replay
    if replay.user != request.user:
        return redirect('forum_replay', pk=replay.sujet.pk)

    # Supprimer le replay
    replay.delete()

    # Rediriger vers le détail du sujet après suppression du replay
    return redirect('forum_replay', pk=replay.sujet.pk)

@login_required
def like_sujet(request, pk):
    sujet = get_object_or_404(Sujet, pk=pk)
    reaction, created = Reaction.objects.get_or_create(user=request.user, sujet=sujet)

    if not created and reaction.reaction == 'like':
        
        reaction.delete()
    else:
      
        reaction.reaction = 'like'
        reaction.save()

    return redirect('forum_replay', pk=sujet.pk)
@login_required
def dislike_sujet(request, pk):
    sujet = get_object_or_404(Sujet, pk=pk)
    reaction, created = Reaction.objects.get_or_create(user=request.user, sujet=sujet)

    if not created and reaction.reaction == 'dislike':
        # Si l'utilisateur a déjà disliké, on annule le dislike
        reaction.delete()
    else:
        # Met à jour ou crée une réaction 'dislike'
        reaction.reaction = 'dislike'
        reaction.save()

    return redirect('forum_replay', pk=sujet.pk)

@login_required
def replay_edit(request, pk):
    replay = get_object_or_404(ReplaySujet, pk=pk)

    # Vérifier que seul l'utilisateur qui a posté le replay peut l'éditer
    if replay.user != request.user:
        return redirect('forum_replay', pk=replay.sujet.pk)

    if request.method == 'POST':
        form = ReplayForm(request.POST, instance=replay)
        if form.is_valid():
            form.save()
            return redirect('forum_replay', pk=replay.sujet.pk)  # Redirige vers le sujet
    else:
        form = ReplayForm(instance=replay)

    return render(request, 'replay_edit.html', {'form': form, 'replay': replay})