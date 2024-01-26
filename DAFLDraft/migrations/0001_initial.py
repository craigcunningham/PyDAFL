# Generated by Django 4.2.1 on 2023-05-10 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('eligible_positions', models.CharField(max_length=30)),
                ('fangraphs_id', models.CharField(max_length=30)),
                ('cbs_id', models.IntegerField()),
                ('mlb_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DAFLDraft.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('P', 'P'), ('C', 'C'), ('1B', '1B'), ('2B', '2B'), ('3b', '3B'), ('SS', 'SS'), ('OF', 'OF'), ('U', 'U')], max_length=2)),
                ('salary', models.IntegerField()),
                ('contract_year', models.IntegerField()),
                ('active', models.BooleanField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DAFLDraft.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DAFLDraft.team')),
            ],
        ),
    ]
