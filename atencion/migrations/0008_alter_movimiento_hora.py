# Generated by Django 5.1.1 on 2024-11-27 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atencion', '0007_alter_movimiento_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='hora',
            field=models.TimeField(default='11:39:55'),
        ),
    ]