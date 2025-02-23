from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)


# class Profile(models.Model):
#     phone = models.CharField(max_length=20)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


# class AdvUser(AbstractUser):
#     phone = models.CharField(max_length=20)


# class AdvUser(User):
#     phone = models.CharField(max_length=20)
#
#     class Meta:
#         proxy = True


class Spare(models.Model):
    name = models.CharField(max_length=30)
    notes = GenericRelation('Note', related_query_name='spare')


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare, through='Kit',
                                    through_fields=('machine', 'spare'))
    notes = GenericRelation('Note')


class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.IntegerField()


class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',
                                       fk_field='object_id')


# 1. Прямое наследование
# class Message(models.Model):
#     content = models.TextField()
#     published = models.DateTimeField(auto_now_add=True, db_index=True)
#
#     class Meta:
#         ordering = ['-published']
#
#
# class PrivateMessage(Message):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.OneToOneField(Message, on_delete=models.CASCADE,
#                                    parent_link=True)
#
#     class Meta:
#         ordering = []


# 2. Абстрактные модели
# class Message(models.Model):
#     content = models.TextField()
#     name = models.CharField(max_length=20)
#     email = models.EmailField()
#
#     class Meta:
#         abstract = True
#         # ordering = ['name']
#
#
# class PrivateMessage(Message):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=40)
#     email = None
#
#     # class Meta:
#         # ordering = ['order', 'name']

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.IntegerField(verbose_name="Количество на складе")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if self.stock < 0:
            raise ValueError("Количество на складе не может быть отрицательным")
        super().save(*args, **kwargs)

    def is_available(self):
        return self.stock > 0


class ElectronicProduct(Product):
    warranty_months = models.IntegerField(default=12, verbose_name="Гарантия (месяцы)")
    brand = models.CharField(max_length=100, verbose_name="Бренд")
    power_consumption = models.FloatField(verbose_name="Потребляемая мощность (Вт)")

    class Meta:
        verbose_name = "Электронный продукт"
        verbose_name_plural = "Электронные продукты"

    def save(self, *args, **kwargs):
        if self.power_consumption < 0:
            raise ValueError("Потребляемая мощность не может быть отрицательной")
        if self.warranty_months < 0:
            raise ValueError("Гарантия не может быть отрицательной")
        super().save(*args, **kwargs)

    def get_warranty_info(self):
        return f"Гарантия: {self.warranty_months} месяцев"


class Smartphone(ElectronicProduct):
    screen_size = models.FloatField(verbose_name="Размер экрана (дюймы)")
    battery_capacity = models.IntegerField(verbose_name="Емкость батареи (мАч)")
    os = models.CharField(max_length=50, verbose_name="Операционная система")

    class Meta:
        verbose_name = "Смартфон"
        verbose_name_plural = "Смартфоны"

    def save(self, *args, **kwargs):
        if self.screen_size < 0:
            raise ValueError("Размер экрана не может быть отрицательным")
        if self.battery_capacity < 0:
            raise ValueError("Емкость батареи не может быть отрицательной")
        super().save(*args, **kwargs)

    def get_full_specs(self):
        return (f"{self.name} ({self.brand})\n"
                f"Экран: {self.screen_size} дюймов\n"
                f"Батарея: {self.battery_capacity} мАч\n"
                f"ОС: {self.os}\n"
                f"Цена: {self.price} тенге")


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('hide_comments', 'Можно скрывать комментарии'),
        )
