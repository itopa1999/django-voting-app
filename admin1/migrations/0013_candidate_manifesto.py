# Generated by Django 4.1.3 on 2022-11-14 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0012_alter_votes_candidate_alter_votes_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='manifesto',
            field=models.TextField(blank=True, max_length=350, null=True),
        ),
    ]
