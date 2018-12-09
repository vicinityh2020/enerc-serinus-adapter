from djongo import models
from django import forms

# Create your models here.


class Sensor(models.Model):
    sensor_type = models.CharField(max_length=255)
    voltage = models.FloatField()
    rssi = models.IntegerField()

    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class MetaData(models.Model):
    # system_id = models.GenericIPAddressField(protocol='IPv4')
    # origin_id = models.GenericIPAddressField(protocol='IPv4')
    # gateway_mac = models.CharField(max_length=17)
    # hardware_version = models.CharField(max_length=100)
    software_version = models.CharField(max_length=100)
    # hop_counter = models.IntegerField()
    # packet_type = models.SmallIntegerField()
    # origin_network_level = models.SmallIntegerField()
    # latency_counter = models.SmallIntegerField()
    message_counter = models.IntegerField()

    class Meta:
        abstract = True


class DecimalRecord(models.Model):
    sensor = models.EmbeddedModelField(
        model_container=Sensor,
    )

    meta_data = models.EmbeddedModelField(
        model_container=MetaData,
    )

    value = models.DecimalField(max_digits=50, decimal_places=10)
    timestamp = models.DateTimeField()

    objects = models.DjongoManager()


class MovementRecord(models.Model):
    sensor = models.EmbeddedModelField(
        model_container=Sensor,
    )

    meta_data = models.EmbeddedModelField(
        model_container=MetaData,
    )

    value = models.BooleanField()
    timestamp = models.DateTimeField()

    objects = models.DjongoManager()


class CO2Record(models.Model):
    sensor = models.EmbeddedModelField(
        model_container=Sensor,
    )

    meta_data = models.EmbeddedModelField(
        model_container=MetaData,
    )

    value = models.IntegerField()
    # timestamp = models.DateTimeField()

    objects = models.DjongoManager()
