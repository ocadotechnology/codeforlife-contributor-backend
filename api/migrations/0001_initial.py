# Generated by Django 3.2.25 on 2024-11-05 12:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.IntegerField(help_text="The contributor's GitHub user-ID.", primary_key=True, serialize=False)),
                ('name', models.TextField(verbose_name='name')),
                ('location', models.TextField(null=True, verbose_name='location')),
                ('html_url', models.TextField(verbose_name='html url')),
                ('avatar_url', models.TextField(verbose_name='avatar url')),
            ],
            options={
                'verbose_name': 'contributor',
                'verbose_name_plural': 'contributors',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='session key')),
                ('session_data', models.TextField(verbose_name='session data')),
                ('expire_date', models.DateTimeField(db_index=True, verbose_name='expire date')),
                ('contributor', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.contributor')),
            ],
            options={
                'verbose_name': 'session',
                'verbose_name_plural': 'sessions',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContributorEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('is_primary', models.BooleanField(verbose_name='is primary')),
                ('is_public', models.BooleanField(verbose_name='is public')),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='api.contributor')),
            ],
            options={
                'verbose_name': 'contributor email',
                'verbose_name_plural': 'contributor emails',
            },
        ),
        migrations.CreateModel(
            name='AgreementSignature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement_id', models.CharField(help_text='Commit ID of the contribution agreement in workspace.', max_length=40, validators=[django.core.validators.MinLengthValidator(40)], verbose_name='agreement id')),
                ('signed_at', models.DateTimeField(verbose_name='signed at')),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreement_signatures', to='api.contributor')),
            ],
            options={
                'verbose_name': 'agreement signature',
                'verbose_name_plural': 'agreement signatures',
            },
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gh_id', models.IntegerField(help_text='Github ID of the repo a contributor has contributed to.', verbose_name='GitHub ID')),
                ('points', models.IntegerField(default=0, help_text='Story points the contributor closed for this repository.', verbose_name='points')),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repositories', to='api.contributor')),
            ],
            options={
                'verbose_name': 'repository',
                'verbose_name_plural': 'repositories',
                'unique_together': {('contributor', 'gh_id')},
            },
        ),
        migrations.AddConstraint(
            model_name='contributoremail',
            constraint=models.UniqueConstraint(condition=models.Q(('is_primary', True)), fields=('contributor',), name='contributor__is_primary'),
        ),
        migrations.AlterUniqueTogether(
            name='agreementsignature',
            unique_together={('contributor', 'agreement_id')},
        ),
    ]
