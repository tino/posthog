# Generated by Django 3.0.6 on 2020-09-17 15:20

import hashlib
import uuid

import django.db.models.deletion
import django.db.models.expressions
from django.conf import settings
from django.db import migrations, models

import posthog.models.utils


def forwards_func(apps, schema_editor):
    User = apps.get_model("posthog", "User")
    Organization = apps.get_model("posthog", "Organization")
    OrganizationMembership = apps.get_model("posthog", "OrganizationMembership")
    Annotation = apps.get_model("posthog", "Annotation")
    for user in User.objects.all():
        team = user.team_set.get()
        deterministic_derived_uuid = uuid.UUID(hashlib.md5(team.id.to_bytes(16, "big")).hexdigest())
        try:
            # try to keep users from the same old team in the same new organization
            user.current_organization = Organization.objects.get(id=deterministic_derived_uuid)
        except Organization.DoesNotExist:
            # if no organization exists for the old team yet, create it
            user.current_organization = Organization.objects.create(id=deterministic_derived_uuid, name=team.name or "Your Organization")
            team.organization = user.current_organization
            team.save()
            for annotation in Annotation.objects.filter(team=team):
                # attach annotations to the new organization
                annotation.organization = user.current_organization
                annotation.scope = "organization" if annotation.apply_all else "dashboard_item"
                annotation.save()
        # migrated users become admins (level 8)
        OrganizationMembership.objects.create(organization=user.current_organization, user=user, level=OrganizationMembership.Level.ADMIN)
        user.current_team = user.current_organization.teams.get()
        user.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("posthog", "0084_person_uuid"),
    ]

    operations = [
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=posthog.models.utils.uuid1_macless, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"abstract": False,},
        ),
        migrations.AddField(
            model_name="annotation",
            name="scope",
            field=models.CharField(
                choices=[
                    ("dashboard_item", "dashboard item"),
                    ("project", "project"),
                    ("organization", "organization"),
                ],
                default="dashboard_item",
                max_length=24,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="current_team",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="teams_currently+",
                to="posthog.Team",
            ),
        ),
        migrations.AlterField(model_name="annotation", name="apply_all", field=models.BooleanField(null=True),),
        migrations.AlterField(
            model_name="annotation",
            name="creation_type",
            field=models.CharField(choices=[("USR", "user"), ("GIT", "GitHub")], default="USR", max_length=3),
        ),
        migrations.AlterField(
            model_name="personalapikey",
            name="team",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="personal_api_keys",
                to="posthog.Team",
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="api_token",
            field=models.CharField(default=posthog.models.utils.generate_random_token, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="team", name="name", field=models.CharField(default="Default", max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="team",
            name="uuid",
            field=models.UUIDField(default=posthog.models.utils.uuid1_macless, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="distinct_id",
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="temporary_token",
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.CreateModel(
            name="OrganizationMembership",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=posthog.models.utils.uuid1_macless, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("level", models.PositiveSmallIntegerField(choices=[(1, "member"), (8, "administrator")], default=1)),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberships",
                        related_query_name="membership",
                        to="posthog.Organization",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_memberships",
                        related_query_name="organization_membership",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrganizationInvite",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=posthog.models.utils.uuid1_macless, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("uses", models.PositiveIntegerField(default=0)),
                ("max_uses", models.PositiveIntegerField(blank=True, default=None, null=True)),
                ("target_email", models.EmailField(blank=True, db_index=True, default=None, max_length=254, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="organization_invites",
                        related_query_name="organization_invite",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_used_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invites",
                        related_query_name="invite",
                        to="posthog.Organization",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="organization",
            name="members",
            field=models.ManyToManyField(
                related_name="organizations",
                related_query_name="organization",
                through="posthog.OrganizationMembership",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="annotation",
            name="organization",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="posthog.Organization"),
        ),
        migrations.AddField(
            model_name="team",
            name="organization",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teams",
                related_query_name="team",
                to="posthog.Organization",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="current_organization",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="users_currently+",
                to="posthog.Organization",
            ),
        ),
        migrations.AddConstraint(
            model_name="organizationmembership",
            constraint=models.UniqueConstraint(
                fields=("organization_id", "user_id"), name="unique_organization_membership"
            ),
        ),
        migrations.AddConstraint(
            model_name="organizationinvite",
            constraint=models.CheckConstraint(
                check=models.Q(uses__lte=django.db.models.expressions.F("max_uses")), name="max_uses_respected"
            ),
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
