# Generated by Django 3.2 on 2021-04-28 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_auto_20210120_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='prediction_model',
            field=models.CharField(choices=[('gpt-2', 'Gpt2'), ('bert', 'Bert'), ('albert', 'Albert'), ('distil-gpt2', 'Dgpt2')], default='GPT2', max_length=15),
        ),
    ]