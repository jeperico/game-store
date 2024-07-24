from django.db import models
from utils.models import DatedModel
from django.conf import settings
from cuser.models import AbstractCUser
import uuid

class User(AbstractCUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100, help_text="Nome do usuário", verbose_name="Nome"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, null=True, blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, editable=False, null=True, blank=True
    )


    class Meta(AbstractCUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def save(self, **kwargs) -> None:
        return super().save(**kwargs)

    def __str__(self):
        return self.email + " | " + self.first_name + " " + self.last_name

class Player(models.Model):
  user = models.OneToOneField(
      settings.AUTH_USER_MODEL,
      help_text="Usuário",
      verbose_name="Usuário",
      on_delete=models.CASCADE,
  )
  name = models.CharField("player's name", max_length=100)
  birthday = models.DateField("player's birthday")

  class Meta:
    verbose_name = "Player"
    verbose_name_plural = "Players"

  def __str__(self):
    return self.name

class Genre(models.Model):
  name = models.CharField("genre's name", max_length=100, null=True, blank=False)
  description = models.TextField("genre's description", blank=True, default="")

  class Meta:
    verbose_name = "Genre"
    verbose_name_plural = "Genres"

  def __str__(self):
    return self.name

class ParentalRating(models.TextChoices):
    E = "E", "Everyone"
    E10 = "E10", "Everyone 10+"
    T = "T", "Teen"
    M = "M", "Mature"
    A = "A", "Adult"


class Games(DatedModel):
  title = models.CharField("game's title", max_length=100, blank=False) # blank=False means that the field is required (default)
  parental_rating = models.CharField("game's parent rating", max_length=3, choices=ParentalRating.choices, default=ParentalRating.E)
  price = models.IntegerField("game's price", default=0)
  description = models.TextField("game's description", blank=True)
  release_date = models.DateField("game's release date", null=True)
  slug = models.SlugField("game's slug", max_length=100, unique=True, null=True, blank=True)
  category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='products', null=True, blank=True)
  player = models.ManyToManyField("Player")
  genre = models.ManyToManyField("Genre")

  class Meta:
    verbose_name = "Game"
    verbose_name_plural = "Games"

  def __str__(self):
    return self.title

class Category(models.Model):
  name = models.CharField("category's name", max_length=100)
  description = models.TextField("category's description", blank=True, default="")

  class Meta:
    verbose_name = "Category"
    verbose_name_plural = "Categories"

  def __str__(self):
    return self.name