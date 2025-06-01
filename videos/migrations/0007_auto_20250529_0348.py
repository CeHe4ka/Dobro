from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('videos', '0006_alter_video_youtube_url'),  # замени на свою последнюю миграцию
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE videos_watchlater
                ALTER COLUMN added_at SET DEFAULT now();
            """,
            reverse_sql="""
                ALTER TABLE videos_watchlater
                ALTER COLUMN added_at DROP DEFAULT;
            """
        ),
    ]
