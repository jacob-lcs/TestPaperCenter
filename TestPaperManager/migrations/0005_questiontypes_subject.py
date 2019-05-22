# Generated by Django 2.0.1 on 2019-05-21 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TestPaperManager', '0004_question_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiontypes',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='type', to='TestPaperManager.Subject', verbose_name='学科'),
            preserve_default=False,
        ),
    ]