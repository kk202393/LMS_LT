# Generated by Django 4.1 on 2023-04-23 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("LOAN", "0066_center_charfield1_center_charfield10_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="center",
            name="Charfield1",
        ),
        migrations.RemoveField(
            model_name="center",
            name="Charfield10",
        ),
    ]