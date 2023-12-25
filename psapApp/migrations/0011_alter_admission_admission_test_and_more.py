# Generated by Django 4.2 on 2023-12-24 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psapApp', '0010_alter_admission_admission_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='admission_test',
            field=models.CharField(choices=[('Not required', 'Not required'), ('NTS NAT', 'NTS NAT'), ('ECAT', 'ECAT'), ('MCAT', 'MCAT')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appliedforadmissionform',
            name='required_test',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]