from django.db import models

class DataModel(models.Model):
    date = models.CharField(max_length=30)
    gender = models.CharField(max_length=50)
    age = models.CharField(max_length=20)
    count = models.CharField(max_length=50)
    # Add more fields as needed

    class Meta:
        managed = False
        db_table = 'gender_data'