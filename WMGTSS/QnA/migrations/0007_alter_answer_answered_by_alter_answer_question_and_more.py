# Generated by Django 4.0.1 on 2022-02-04 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QnA', '0006_question_answered_alter_answer_answered_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answered_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='answered_by', to='QnA.profile'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='QnA.question'),
        ),
        migrations.AlterField(
            model_name='board',
            name='viewers',
            field=models.ManyToManyField(related_name='viewable_by', to='QnA.Profile'),
        ),
    ]
