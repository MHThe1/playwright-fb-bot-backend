# Generated by Django 5.1.3 on 2024-11-30 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_alter_action_action_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='is_assigning',
            field=models.BooleanField(default=True),
        ),
    ]