# Generated by Django 5.0.6 on 2024-06-17 21:15

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='upload',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=1, verbose_name='Загрузка файла'),
            preserve_default=False,
        ),
    ]
