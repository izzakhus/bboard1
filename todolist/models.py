from django.db import models


# class Todo(models.Model):
#     title = models.CharField(
#         max_length=50,
#         verbose_name='Задача',
#     )


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title