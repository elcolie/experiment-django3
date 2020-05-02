from django.contrib.postgres.fields import DecimalRangeField
from django.db import models


class Premium(models.Model):
    percentage = models.DecimalField(max_digits=10, decimal_places=2)
    sum_insured = DecimalRangeField()   # Insurer accepts this range

    def __str__(self):
        return f"{self.percentage} | {self.sum_insured}"
