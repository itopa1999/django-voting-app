# Generated by Django 3.2.4 on 2022-11-02 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0004_remove_votes_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
