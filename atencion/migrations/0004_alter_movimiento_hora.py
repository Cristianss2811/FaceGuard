# Generated by Django 5.1.1 on 2024-11-09 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atencion', '0003_alter_movimiento_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='hora',
            field=models.TimeField(default='00:22:53'),
        ),
    ]