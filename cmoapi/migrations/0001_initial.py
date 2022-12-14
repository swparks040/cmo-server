# Generated by Django 4.1.4 on 2023-01-05 19:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CMOUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_position', models.TextField()),
                ('salary', models.BigIntegerField()),
                ('birthday', models.DateField()),
                ('date_hired', models.DateField()),
                ('date_evaluated', models.DateField()),
                ('date_promoted', models.DateField()),
                ('profile_image_url', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMemberRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PTO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_days', models.IntegerField()),
                ('days_used', models.IntegerField()),
                ('days_remaining', models.IntegerField()),
                ('cmouser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmoapi.cmouser')),
            ],
        ),
        migrations.CreateModel(
            name='PTORequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('days_requested', models.IntegerField()),
                ('justification', models.CharField(max_length=275)),
                ('is_approved', models.BooleanField(default=False)),
                ('cmouser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmoapi.cmouser')),
                ('pto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmoapi.pto')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('publication_date', models.DateField(default=datetime.date.today)),
                ('content', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmoapi.category')),
                ('cmouser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmoapi.cmouser')),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('birthday', models.CharField(max_length=50)),
                ('anniversary', models.CharField(max_length=50)),
                ('graduation', models.CharField(max_length=50)),
                ('cmouser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmoapi.cmouser')),
                ('family_member_relationship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmoapi.familymemberrelationship')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_on', models.DateField(default=datetime.date.today)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmoapi.cmouser')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmoapi.message')),
            ],
        ),
    ]
