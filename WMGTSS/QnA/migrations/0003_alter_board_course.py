# Generated by Django 4.0.1 on 2022-02-02 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QnA', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QnA.course'),
        ),
    ]
