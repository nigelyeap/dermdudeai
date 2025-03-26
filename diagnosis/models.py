from django.db import models

class DermaCase(models.Model):
    image = models.ImageField(upload_to='', null=True, blank=True)
    diagnosis = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"Case {self.id}: {self.diagnosis[:50]}"