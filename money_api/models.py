from django.db import models
from django.contrib.auth.models import User

class FinancialRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()  # 1–12
    amount = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.year}/{self.month}: {self.amount}"
