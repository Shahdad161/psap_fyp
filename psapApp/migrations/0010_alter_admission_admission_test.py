# Generated by Django 4.2 on 2023-12-24 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psapApp', '0009_admission_is_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='admission_test',
            field=models.CharField(blank=True, choices=[('Not required', 'Not required'), ('NTS NAT', 'NTS NAT'), ('ECAT', 'ECAT'), ('MCAT', 'MCAT')], max_length=20, null=True),
        ),
    ]