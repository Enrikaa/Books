from django.db import models

from UsersApp.models import User


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, help_text="First name and Last Name")
    publication_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-publication_date"]

    def __str__(self):
        return self.title
