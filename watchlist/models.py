from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Watchlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    assets = models.JSONField()
    name = models.CharField(max_length=50) # a user can have multiple watchlists to toggle between
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_watchlist')
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            if Watchlist.objects.filter(user=self.user, name=self.name).exists():
                raise ValidationError(f"A watchlist with the name '{self.name}' already exists for this user.")
        super(Watchlist, self).save(*args, **kwargs)