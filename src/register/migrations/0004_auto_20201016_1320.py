# Generated by Django 3.0.7 on 2020-10-16 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_auto_20200929_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='prediction_model',
            field=models.CharField(choices=[('gpt-2', 'Gpt2'), ('bert', 'Bert'), ('albert', 'Albert'), ('distil-gpt2', 'Dgpt2')], default='GPT2', max_length=15),
        ),
    ]