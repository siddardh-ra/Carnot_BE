from django.db import models
from django.contrib.auth.models import Group
from Users.models import UserProfile
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, default="")
    city = models.CharField(max_length=20, default="")
    state = models.CharField(max_length=20, default="")
    country = models.CharField(max_length=20, default="")
    table_type = models.CharField(max_length=20, default="")
    inverter_type = models.CharField(max_length=20, default="")
    module_type = models.CharField(max_length=20, default="")
    plant_size = models.CharField(
        default="", max_length=50, blank=True, null=True)
    plant_capacity = models.CharField(max_length=20, default="")
    category = models.CharField(max_length=100, default="", choices=(('thermography', 'thermography'), ('topography', 'topography'),
                                                                     ('grading', 'grading'), ('due diligence', 'due diligence')), null=True, blank=True)
    zoom_level = models.CharField(
        max_length=10, default="15", null=True, blank=True)
    project_created_date = models.DateField()
    center = models.CharField(
        max_length=255, default="", null=True, blank=True)
    organization = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='org')
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    properties = models.TextField(default="{}")
    project_dates = models.TextField(default="{}")
    status = models.CharField(max_length=50, choices=(('created', 'created'), ('ftp', 'ftp'), (
        'processing', 'processing'), ('completed', 'completed')), default="created")
    clients = models.ManyToManyField(Group, related_name='client')
    shared_profile = models.ManyToManyField(
        User, related_name='shared_profile')

    def __str__(self):
        return self.name + "_" + self.plant_capacity


class ProjectProcessedData(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField()
    ortho_file_location = models.CharField(
        max_length=255, default="", null=True, blank=True)
    kml_file_location = models.CharField(
        max_length=255, default="", null=True, blank=True)
    cad_file_location = models.CharField(
        max_length=255, default="", null=True, blank=True)
    thermal_hotspot_location = models.CharField(
        max_length=255, default="", null=True, blank=True)
    dtm_legend = models.CharField(
        max_length=255, default="", null=True, blank=True)
    slope_legend = models.CharField(
        max_length=255, default="", null=True, blank=True)
    csv_path = models.CharField(
        max_length=255, default="", null=True, blank=True)
    grading_layers = models.TextField(default="{}", blank=True, null=True)
    summary_layers = models.TextField(default="{}", blank=True, null=True)
    inverter_layers = models.TextField(default="{}", blank=True, null=True)
    topography_layers = models.TextField(default="{}", blank=True, null=True)
    power_loss = models.TextField(default="{}", blank=True, null=True)
    properties = models.TextField(default="{}")
    total_modules_present = models.CharField(max_length=20, default="0")
    plant_size_scanned = models.CharField(max_length=20, default="0")
    total_power_loss = models.CharField(max_length=20, default="0")
    total_defects = models.CharField(max_length=20, default="0")
    report_path = models.CharField(
        max_length=255, default="", null=True, blank=True)
    status = models.CharField(max_length=50, choices=(('created', 'created'), ('ftp', 'ftp'), (
        'processing', 'processing'), ('completed', 'completed')), default="created")

    def __str__(self):
        return self.project.name + "_" + str(self.date)


class ProjectData(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.ForeignKey(ProjectProcessedData, on_delete=models.CASCADE)
    properties = models.TextField(default="{}")
    environmental_condition = models.TextField(
        default="{}", null=True, blank=True)
    payload_check = models.TextField(default="{}", null=True, blank=True)

    def __str__(self):
        return self.project.name
