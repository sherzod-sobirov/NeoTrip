from django.db import models


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)  # Bu maydonni tekshiring
    profile_image = models.ImageField(upload_to='team_members/')
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name



class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=13)
    comment = models.TextField()

    def __str__(self):
        return f"{self.first_name}"


class BannerImg(models.Model):
    photo = models.ImageField(upload_to="static/images/")

    def __str__(self) -> str:
        return self.photo


class Comment(models.Model):
    name = models.CharField(max_length=255)
    message = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.created_at}"