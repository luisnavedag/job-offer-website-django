from django.db import models


class CommonItem(models.Model):
    """
    An abstract class for extending classes in the model
    """
    name = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True