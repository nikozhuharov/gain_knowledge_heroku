# Generated by Django 4.0.3 on 2022-03-13 16:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import gain_knowledge.main.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2)])),
                ('picture', models.ImageField(upload_to='images/category', validators=[gain_knowledge.main.validators.MaxFileSizeInMbValidator(5)])),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2)])),
                ('description', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(upload_to='images/course', validators=[gain_knowledge.main.validators.MaxFileSizeInMbValidator(5)])),
                ('video', models.FileField(blank=True, null=True, upload_to='videos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
                ('document', models.FileField(upload_to='documents', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answers', models.IntegerField()),
                ('incorrect_answers', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2)])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('first_option', models.TextField()),
                ('second_option', models.TextField()),
                ('third_option', models.TextField()),
                ('fourth_option', models.TextField()),
                ('correct_answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.test')),
            ],
        ),
    ]
