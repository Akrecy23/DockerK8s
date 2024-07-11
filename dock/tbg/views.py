from django.shortcuts import render, redirect
from .models import Game
from random import choice

def index(request):
    game, created = Game.objects.get_or_create(id=1)
    if request.method == 'POST':
        user_action = request.POST.get('action')
        enemy_action = choice(['attack', 'defense', 'recovery'])

        if game.game_over:
            return render(request, 'tbg/index.html', {'game': game})

        if user_action == 'attack':
            if enemy_action != 'defense':
                game.enemy_health -= 10
            if enemy_action == 'attack':
                game.user_health -= 5
        elif user_action == 'defense':
            if enemy_action == 'attack':
                game.user_health -= 2
        elif user_action == 'recovery':
            game.user_health += 5
            if enemy_action == 'attack':
                game.user_health -= 5

        if game.user_health <= 0:
            game.user_health = 0
            game.game_over = True
            game.winner = 'Enemy'

        if game.enemy_health <= 0:
            game.enemy_health = 0
            game.game_over = True
            game.winner = 'User'

        game.save()

    return render(request, 'tbg/index.html', {'game': game})

def reset(request):
    game = Game.objects.get(id=1)
    game.user_health = 100
    game.enemy_health = 500
    game.user_action = None
    game.enemy_action = None
    game.game_over = False
    game.winner = None
    game.save()
    return redirect('index')
