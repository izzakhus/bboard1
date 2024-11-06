from django.db import models


class Rubric(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = "Рубрики"

    def __str__(self):
        return f'{self.name}'


class Bb(models.Model):
    # KINDS = (
    # ('b', 'Куплю',),
    # ('d', 'Продам'),
    # ('c', 'Обменяю'),
    # )
    KINDS = (
        (None, 'Выберите тип публикуемого объявления'),
        ('b', 'Куплю',),
        ('d', 'Продам'),
        ('c', 'Обменяю'),
    )
    # KINDS = (
    #     ('Куплю продажа', (
    #         ('b', 'Куплю'),
    #         ('d', 'Продам'),
    #     )),
    #     ('Обмен', (
    #         ('c', 'Обменяю'),
    #     ))
    # )
    kind = models.CharField(
        max_length=1,
        choices=KINDS,
        default='s',
    )
    rubric = models.ForeignKey(
        verbose_name='Рубрика',
        to='Rubric', null=True,
        on_delete=models.PROTECT
    )
    title = models.CharField(
        verbose_name='Товар',
        max_length=50
    )
    content = models.TextField(
        verbose_name='Контент',
        null=True, blank=True
    )
    # price = models.FloatField(verbose_name='Цена', null=True, blank=True)
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        default=0)
    publisher = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return f'{self.title} {self.price} тг.'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = "Обьявления"
        ordering = ['-publisher', 'title']
        unique_together = ('title', 'publisher')
    # is_active = models.BooleanField()
