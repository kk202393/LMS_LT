# Generated by Django 4.1 on 2023-01-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LOAN", "0048_alter_cashbookreport_branch"),
    ]

    operations = [
        migrations.AddField(
            model_name="cashbookreport",
            name="_20Coin",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]