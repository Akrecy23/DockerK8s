import random
from django.shortcuts import render

def home(request):
    return render(request, 'rps/home.html')

def play(request):
    choices = ['rock', 'paper', 'scissors']
    player_choice = request.POST.get('choice')
    computer_choice = random.choice(choices)
    
    if player_choice == computer_choice:
        result = 'It\'s a tie!'
    elif (player_choice == 'rock' and computer_choice == 'scissors') or \
         (player_choice == 'scissors' and computer_choice == 'paper') or \
         (player_choice == 'paper' and computer_choice == 'rock'):
        result = 'You win!'
    else:
        result = 'You lose!'
    
    context = {
        'player_choice': player_choice,
        'computer_choice': computer_choice,
        'result': result,
    }
    return render(request, 'rps/result.html', context)
