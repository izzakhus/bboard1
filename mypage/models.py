from django.db import models


class Review(models.Model):
    comment = models.CharField(
        unique=True,
        max_length=20,
        db_index=True,
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
