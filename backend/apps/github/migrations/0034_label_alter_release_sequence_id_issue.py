# Generated by Django 5.1.1 on 2024-09-04 00:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("github", "0033_alter_release_repository"),
    ]

    operations = [
        migrations.CreateModel(
            name="Label",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("nest_created_at", models.DateTimeField(auto_now_add=True)),
                ("nest_updated_at", models.DateTimeField(auto_now=True)),
                ("node_id", models.CharField(unique=True, verbose_name="Node ID")),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                ("description", models.CharField(max_length=200, verbose_name="Description")),
                ("color", models.CharField(default="", max_length=6, verbose_name="Color")),
                (
                    "sequence_id",
                    models.PositiveBigIntegerField(default=0, verbose_name="Label ID"),
                ),
                ("is_default", models.BooleanField(default=False, verbose_name="Is default")),
            ],
            options={
                "verbose_name_plural": "Labels",
                "db_table": "github_labels",
            },
        ),
        migrations.AlterField(
            model_name="release",
            name="sequence_id",
            field=models.PositiveBigIntegerField(default=0, verbose_name="Release ID"),
        ),
        migrations.CreateModel(
            name="Issue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("nest_created_at", models.DateTimeField(auto_now_add=True)),
                ("nest_updated_at", models.DateTimeField(auto_now=True)),
                ("node_id", models.CharField(unique=True, verbose_name="Node ID")),
                ("title", models.CharField(max_length=200, verbose_name="Title")),
                ("body", models.TextField(default="", verbose_name="Body")),
                (
                    "state",
                    models.CharField(
                        choices=[("open", "Open")],
                        default="open",
                        max_length=20,
                        verbose_name="State",
                    ),
                ),
                ("url", models.URLField(default="", verbose_name="URL")),
                ("number", models.PositiveBigIntegerField(default=0, verbose_name="Number")),
                (
                    "sequence_id",
                    models.PositiveBigIntegerField(default=0, verbose_name="Issue ID"),
                ),
                ("is_locked", models.BooleanField(default=False, verbose_name="Is locked")),
                (
                    "lock_reason",
                    models.CharField(default="", max_length=200, verbose_name="Lock reason"),
                ),
                (
                    "comments_count",
                    models.PositiveIntegerField(default=0, verbose_name="Comments"),
                ),
                ("created_at", models.DateTimeField(verbose_name="Created at")),
                ("updated_at", models.DateTimeField(verbose_name="Updated at")),
                (
                    "assignee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_issues",
                        to="github.user",
                        verbose_name="Assignee",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_issues",
                        to="github.user",
                        verbose_name="Author",
                    ),
                ),
                (
                    "repository",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="issues",
                        to="github.repository",
                    ),
                ),
                (
                    "labels",
                    models.ManyToManyField(
                        blank=True, related_name="+", to="github.label", verbose_name="Labels"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Issues",
                "db_table": "github_issues",
            },
        ),
    ]