# Generated by Django 4.1 on 2023-05-10 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LOAN", "0094_alter_banktransactions_accountnumber"),
    ]

    operations = [
        migrations.AlterField(
            model_name="banktransactions",
            name="TransactionsDate",
            field=models.DateTimeField(),
        ),
    ]