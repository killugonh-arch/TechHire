from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extends the built-in User model to track membership tier.
    Basic members see locked fields; Premium members see everything.
    """
    BASIC = 'basic'
    PREMIUM = 'premium'
    TIER_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    membership_tier = models.CharField(max_length=10, choices=TIER_CHOICES, default=BASIC)

    @property
    def is_premium(self):
        return self.membership_tier == self.PREMIUM

    def __str__(self):
        return f"{self.user.username} ({self.get_membership_tier_display()})"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create a UserProfile whenever a new User is created."""
    if created:
        UserProfile.objects.get_or_create(user=instance)


class JobPosting(models.Model):
    """
    A job listing on the TechHire board.
    Premium-only fields: company_name, salary_range, application_link.
    """
    # Public fields (visible to all users)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    # Premium-only fields
    company_name = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=100, help_text="e.g. $120,000 – $160,000")
    application_link = models.URLField(max_length=500)

    class Meta:
        ordering = ['-created_at']  # Newest first by default

    def __str__(self):
        return f"{self.title} @ {self.company_name}"