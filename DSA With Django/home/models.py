from django.db import models
import hashlib
import random

def generate_hash(long_url, user_email):
    """
    Generate a 6-character hash based on the long URL and user's email.
    """
    hash_object = hashlib.md5(f"{long_url}{user_email}".encode())
    return hash_object.hexdigest()[:6]

class URL(models.Model):
    # Auto-incrementing link ID
    link_id = models.AutoField(primary_key=True)

    # User email to associate links
    user_email = models.EmailField()

    # Original URL
    long_url = models.URLField(max_length=1000)

    # Short URL (unique per user)
    short_url = models.CharField(max_length=100, unique=True, blank=True)

    # Hash for lookup (unique per user)
    url_hash = models.CharField(max_length=100, blank=True)

    # Creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    # Position in SLL (for maintaining order) - add default value
    sll_position = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Generate a unique hash per user if not already set
        if not self.url_hash:
            hash_code = generate_hash(self.long_url, self.user_email)

            # Check for collision for this user
            while URL.objects.filter(user_email=self.user_email, url_hash=hash_code).exists():
                # Append random number to avoid collision
                hash_code = generate_hash(self.long_url + str(random.randint(0, 9999)), self.user_email)

            self.url_hash = hash_code

        # Generate short URL if not already set
        if not self.short_url:
            self.short_url = f"shorten.ly/{self.url_hash}"

        # Set SLL position if not set (only for new objects)
        if self.pk is None:  # Only for new objects
            max_position = URL.objects.filter(user_email=self.user_email).aggregate(
                models.Max('sll_position')
            )['sll_position__max'] or 0
            self.sll_position = max_position + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f" user: {self.user_email} | {self.long_url} -> {self.short_url}"