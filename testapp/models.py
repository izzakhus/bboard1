from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, AbstractUser
from django.db import models, transaction
from django.core.exceptions import ValidationError


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
class Message(models.Model):
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-published']


class PrivateMessage(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.OneToOneField(Message, on_delete=models.CASCADE,
                                   parent_link=True)

    class Meta:
        ordering = []


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


class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.IntegerField(verbose_name="Количество на складе")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if self.stock < 0:
            raise ValueError("Количество на складе не может быть отрицательным")
        super().save(*args, **kwargs)


class OrderQuerySet(models.QuerySet):
    def active(self):

        return self.filter(is_cancelled=False)

    def recent(self):
        from django.utils import timezone
        from datetime import timedelta
        return self.filter(created_at__gte=timezone.now() - timedelta(days=7))


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def create_order(self, item, quantity):
        if quantity < 1:
            raise ValidationError("Количество должно быть положительным")
        if item.stock < quantity:
            raise ValidationError("Недостаточно товара на складе")

        order = self.model(item=item, quantity=quantity)
        order.total_price = item.price * quantity
        with transaction.atomic():
            item.stock -= quantity
            item.save()
            order.save()
        return order


class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(verbose_name="Количество")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_cancelled = models.BooleanField(default=False, verbose_name="Отменен")

    objects = OrderManager()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ {self.item.name} ({self.quantity} шт.)"

    def save(self, *args, **kwargs):
        if self.quantity < 1:
            raise ValueError("Количество должно быть положительным")
        if not self.pk and not self.is_cancelled:  # Новый заказ
            self.total_price = self.item.price * self.quantity
            if self.item.stock < self.quantity:
                raise ValidationError("Недостаточно товара на складе")
            self.item.stock -= self.quantity
            self.item.save()
        super().save(*args, **kwargs)

    def cancel_order(self):
        if self.is_cancelled:
            raise ValidationError("Заказ уже отменен")
        with transaction.atomic():
            self.is_cancelled = True
            self.item.stock += self.quantity
            self.item.save()
            self.save()
        return f"Заказ {self} успешно отменен"


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('hide_comments', 'Можно скрывать комментарии'),
        )
