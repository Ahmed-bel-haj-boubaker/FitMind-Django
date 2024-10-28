# Generated by Django 5.1.2 on 2024-10-27 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmicalculator', '0006_nutritionplan_bmicalculator_nutrition_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nutritionplan',
            name='carbs_percentage',
        ),
        migrations.RemoveField(
            model_name='nutritionplan',
            name='daily_calories',
        ),
        migrations.RemoveField(
            model_name='nutritionplan',
            name='description',
        ),
        migrations.RemoveField(
            model_name='nutritionplan',
            name='fats_percentage',
        ),
        migrations.RemoveField(
            model_name='nutritionplan',
            name='name',
        ),
        migrations.RemoveField(
            model_name='nutritionplan',
            name='protein_percentage',
        ),
        migrations.AddField(
            model_name='nutritionplan',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
