from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cine_verse', '0002_remove_userprofile_favorite_genre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='content_type',
            field=models.CharField(choices=[('movie', 'Movie'), ('series', 'Series')], default='movie', max_length=20),
        ),
    ]