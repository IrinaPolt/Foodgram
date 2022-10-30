from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
USER = 'user'


CHOICES = (
    (USER, 'user'),
    (ADMIN, 'admin'),
)


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=150, choices=CHOICES, default=USER)
    password = models.CharField(max_length=150)
    is_subscribed = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_admin(self):
        return self.role == ADMIN


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['author', ]
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'], name='unique_subscription')
        ]
