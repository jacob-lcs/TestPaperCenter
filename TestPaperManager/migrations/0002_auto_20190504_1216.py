# Generated by Django 2.2.1 on 2019-05-04 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TestPaperManager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='subject',
        ),
        migrations.AddField(
            model_name='paper',
            name='subject_name',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='TestPaperManager.Subject', verbose_name='科目名称'),
            preserve_default=False,
        ),
    ]