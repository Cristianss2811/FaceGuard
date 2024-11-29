# Generated by Django 5.1.1 on 2024-11-25 03:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('areas', '0003_zona_zonasareas_area_zonas'),
        ('atencion', '0005_alter_movimiento_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='hora',
            field=models.TimeField(default='21:03:07'),
        ),
        migrations.AlterField(
            model_name='puertamovimiento',
            name='movimiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atencion.movimiento'),
        ),
        migrations.AlterField(
            model_name='puertamovimiento',
            name='puerta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='areas.puerta'),
        ),
    ]