from django.db import models


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name


class Store(models.Model):
    id = models.AutoField(primary_key=True)
    place_id = models.TextField()
    name = models.TextField()
    address = models.TextField()
    phone = models.TextField()
    picture = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()
    website = models.TextField(null=True)
    star = models.FloatField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    tag = models.ForeignKey(Tag, on_delete=models.PROTECT, related_name='tag')

    class Meta:
        db_table = 'store'

    def __str__(self):
        return self.name
