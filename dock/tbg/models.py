from django.db import models

class Game(models.Model):
    user_health = models.IntegerField(default=100)
    enemy_health = models.IntegerField(default=500)
    user_action = models.CharField(max_length=10, null=True, blank=True)
    enemy_action = models.CharField(max_length=10, null=True, blank=True)
    game_over = models.BooleanField(default=False)
    winner = models.CharField(max_length=10, null=True, blank=True)
