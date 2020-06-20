# Generated by Django 3.0.7 on 2020-06-20 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0002_comment_group_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=4096)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.TextField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='is_book',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='is_lost',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.CreateModel(
            name='UserToCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='tgbot.Category')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='tgbot.User')),
            ],
        ),
    ]
