# Generated by Django 3.0.7 on 2020-09-21 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='prediction_model',
            field=models.CharField(choices=[('gpt-2', 'Gpt2'), ('bert', 'Bert'), ('albert', 'Albert')], default='gpt-2', max_length=6),
        ),
    ]
