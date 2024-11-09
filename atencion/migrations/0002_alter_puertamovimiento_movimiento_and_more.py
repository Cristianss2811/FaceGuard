# Generated by Django 5.1.1 on 2024-10-31 04:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('areas', '0001_initial'),
        ('atencion', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='puertamovimiento',
            name='movimiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='areas.puerta'),
        ),
        migrations.AlterField(
            model_name='puertamovimiento',
            name='puerta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usuariomovimiento',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]