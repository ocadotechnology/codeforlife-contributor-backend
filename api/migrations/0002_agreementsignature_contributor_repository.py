# Generated by Django 3.2.25 on 2024-07-09 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('name', models.TextField()),
                ('location', models.TextField()),
                ('html_url', models.TextField()),
                ('avatar_url', models.TextField()),
            ],
            options={
                'verbose_name': 'contributor',
                'verbose_name_plural': 'contributors',
            },
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField(choices=[('portal', 'portal'), ('rr', 'rr')])),
                ('points', models.IntegerField(default=0)),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.contributor')),
            ],
            options={
                'unique_together': {('contributor', 'name')},
            },
        ),
        migrations.CreateModel(
            name='AgreementSignature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement_id', models.CharField(max_length=40)),
                ('signed_at', models.DateTimeField()),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.contributor')),
            ],
            options={
                'unique_together': {('contributor', 'agreement_id')},
            },
        ),
    ]
