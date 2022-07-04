from rest_framework.serializers import ModelSerializer
from .models import Project, ProjectProcessedData


class ListProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def to_representation(self, instance):
        print("", instance.organization)
        # resp=instance.name
        resp = {"name": instance.name,
                "description": instance.description, "plant_size": instance.plant_size,
                "center": instance.center, "city": instance.city, "state": instance.state,
                "country": instance.country, "project_created_date": instance.project_created_date,
                "organization": str(instance.organization), "status": instance.status
                }
        return resp


class ListStatus_Project(ModelSerializer):
    class Meta:
        model = ProjectProcessedData
        fields = "__all__"

    def to_representation(self, instance):
        print("", instance.organization)
        # resp=instance.name
        resp = {"name": instance.project.name,
                "status": instance.status, "date": instance.date
                }
        return resp
