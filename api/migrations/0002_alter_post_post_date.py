# Generated by Django 4.2.7 on 2023-11-01 08:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="post_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
