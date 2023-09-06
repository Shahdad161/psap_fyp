# Generated by Django 4.2 on 2023-07-26 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psapApp', '0002_admission_campus'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppliedForAdmissionForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university', models.CharField(max_length=100)),
                ('campus', models.CharField(max_length=100)),
                ('program', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('required_test', models.CharField(max_length=100)),
                ('test_obtained_marks', models.IntegerField()),
                ('test_total_marks', models.IntegerField()),
                ('fees_slip', models.FileField(upload_to='fees_slips/')),
                ('student_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psapApp.stdinfotable')),
            ],
        ),
    ]
