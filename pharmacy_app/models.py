from django.db import models
import uuid
from django.urls import reverse


class Medicine(models.Model):
    name = models.CharField(max_length=200, help_text="Medicine name")
    producer = models.CharField(max_length=100, help_text="Medicine producer")
    url = models.CharField(max_length=1000, help_text="Medicine web url")
    category = models.ForeignKey('MedicineCategory', on_delete=models.SET_NULL, null=True)
    date_added = models.DateField(null=True, blank=True)
    date_updated = models.DateField(null=True, blank=True)
    price = models.FloatField(help_text="Medicine price")
    count = models.IntegerField(help_text="Number of available medicine units")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('medicine-detail', args=[str(self.id)])


class MedicineUnit(models.Model):
    medicine = models.ForeignKey('Medicine', on_delete=models.SET_NULL, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for particular medicine unit")

    STATUS = (
        ('s', 'Sold'),
        ('o', 'Ordered'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status = models.CharField(max_length=1, choices=STATUS, blank=True, default='a',
                              help_text="Medicine unit status")
    date_added = models.DateField(null=True, blank=True)
    date_updated = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['medicine']

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.medicine.name)


class MedicineCategory(models.Model):
    name = models.CharField(max_length=100, help_text="Medicine category name")

    class Meta:
        ordering = ['name']
        verbose_name_plural = "medicine categories"

    def __str__(self):
        return self.name


class MedicineSale(models.Model):
    medicine = models.ForeignKey('Medicine', on_delete=models.SET_NULL, null=True)
    items_count = models.IntegerField()
    amount = models.FloatField()
    purchase_date = models.DateField()
    purchase_time = models.TimeField()

    class Meta:
        ordering = ['-purchase_date', '-purchase_time']
