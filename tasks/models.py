from django.contrib.auth.models import User
from django.db import models


class Todo(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # owner
    text = models.CharField(verbose_name="todo text", max_length=400)
    color = models.CharField(verbose_name="color", default="#ffffff", max_length=10)  # background color

    def __str__(self):
        """
        string representation
        """
        return self.text[:15]


class Subtask(models.Model):

    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='subtasks')  # todo parent
    text = models.CharField(verbose_name="subtask text", max_length=400)
    color = models.CharField(verbose_name="color", default="#ffffff", max_length=10)

    def __str__(self):
        """
        string representation
        """
        return self.text[:15]
