# Generated by Django 4.1.3 on 2022-12-22 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0013_candidate_manifesto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votes',
            name='candidate',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='votes',
            name='position',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
