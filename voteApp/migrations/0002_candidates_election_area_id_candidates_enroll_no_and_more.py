# Generated by Django 5.0.3 on 2024-04-17 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voteApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidates',
            name='election_area_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='candidates',
            name='enroll_no',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='candidates',
            name='insert_by',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='candidates',
            name='insert_time',
            field=models.CharField(default='0000-00-00 00:00', max_length=20),
        ),
        migrations.AlterField(
            model_name='candidates',
            name='ballot_no',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='candidates',
            name='name',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='candidates',
            name='photo',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='candidates',
            name='voter_no',
            field=models.IntegerField(default=0),
        ),
    ]
