from django.db import models


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_images/')
    display_order = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.name}"


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
