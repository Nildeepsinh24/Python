from django.conf import settings
from django.db import models


class Genre(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.name


class Movie(models.Model):
	CONTENT_TYPE_CHOICES = [
		('movie', 'Movie'),
		('series', 'Series'),
	]

	title = models.CharField(max_length=255)
	description = models.TextField()
	content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='movie')
	poster_url = models.URLField(max_length=1000)
	banner_url = models.URLField(max_length=1000)
	video_url = models.URLField(max_length=1000, default='https://www.w3schools.com/html/mov_bbb.mp4')
	rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
	release_year = models.IntegerField(default=2024)
	language = models.CharField(max_length=100, default='English')
	duration = models.CharField(max_length=50, default='2h 15m')
	is_trending = models.BooleanField(default=False)
	is_popular = models.BooleanField(default=False)
	is_latest = models.BooleanField(default=False)
	is_top_rated = models.BooleanField(default=False)
	cast = models.TextField(help_text='Comma-separated cast list')
	crew = models.TextField(default='Director: John Doe', help_text='Comma-separated crew list')
	display_order = models.IntegerField(default=0, help_text="Order of displaying in lists")
	genres = models.ManyToManyField(Genre, related_name='movies')

	def __str__(self):
		return self.title


class UserProfile(models.Model):
	SUBSCRIPTION_CHOICES = [
		('Basic', 'Basic'),
		('Standard', 'Standard'),
		('Premium', 'Premium'),
	]

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	subscription_plan = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICES, default='Basic')
	avatar_url = models.URLField(max_length=1000, blank=True, null=True)
	favorite_genres = models.ManyToManyField(Genre, blank=True, related_name='favorited_by_profiles')
	favorites = models.ManyToManyField(Movie, blank=True, related_name='favorited_by')
	watchlist = models.ManyToManyField(Movie, blank=True, related_name='watchlisted_by')
	watchlist_order = models.TextField(blank=True, default='')
	favorites_order = models.TextField(blank=True, default='')

	def __str__(self):
		return f'{self.user.username} profile'


class WatchHistory(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watch_history')
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	watched_at = models.DateTimeField(auto_now=True)
	progress = models.IntegerField(default=0, help_text='Percentage of movie watched (0-100)')

	class Meta:
		ordering = ['-watched_at']
		unique_together = ('user', 'movie')

	def __str__(self):
		return f'{self.user.username} - {self.movie.title}'


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
	try:
		instance.profile.save()
	except UserProfile.DoesNotExist:
		UserProfile.objects.create(user=instance)


