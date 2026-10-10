
from django.db import migrations, models


def copy_approval_to_status(apps, schema_editor):
    Resource = apps.get_model('blog', 'CommunityResource')

    Resource.objects.filter(is_approved=True).update(
        status='approved'
    )
    Resource.objects.filter(is_approved=False).update(
        status='pending'
    )


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0004_communityresource'),
    ]

    operations = [
        migrations.AddField(
            model_name='communityresource',
            name='status',
            field=models.CharField(
                max_length=10,
                choices=[
                    ('pending', 'Pending review'),
                    ('approved', 'Approved'),
                    ('rejected', 'Rejected'),
                ],
                default='pending',
                db_index=True,
            ),
        ),
        migrations.RunPython(
            copy_approval_to_status,
            migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='communityresource',
            name='is_approved',
        ),
    ]
