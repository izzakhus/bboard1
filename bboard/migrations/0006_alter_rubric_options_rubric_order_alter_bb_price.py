# Generated by Django 5.1.2 on 2024-12-18 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0005_merge_20241129_1638'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rubric',
            options={'ordering': ['order', 'name'], 'verbose_name': 'Рубрика', 'verbose_name_plural': 'Рубрики'},
        ),
        migrations.AddField(
            model_name='rubric',
            name='order',
            field=models.SmallIntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='bb',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Цена'),
        ),
    ]
