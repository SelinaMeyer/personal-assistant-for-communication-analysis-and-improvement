from django.db import models

class Chat(models.Model):
    chat_id = models.IntegerField(unique=True)
    chat_text = models.TextField()
    interaction_context = models.TextField(max_length=255)
    victim = models.TextField(max_length=255)
    culprit = models.TextField(max_length=255)
    manipulation_strategy = models.TextField(max_length=255)

class Advice(models.Model):
    advice_id = models.IntegerField(unique=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    advice_text = models.TextField()
    context = models.CharField(max_length=255, default='')  # Added context field
    model = models.CharField(max_length=255, default='')

class Rating(models.Model):
    advice = models.ForeignKey(Advice, on_delete=models.CASCADE)
    prolific_id = models.CharField(max_length=255)
    RATING_CHOICES = [
        ('mistreated', 'I would feel mistreated'),
        ('wrong', 'I would feel like I might have done something wrong'),
        ('neutral', 'I would feel neutral, there is nothing wrong with this conversation'),
    ]

    rating_chat = models.CharField(max_length=255, choices=RATING_CHOICES)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1-5 scale
    text_feedback = models.TextField()