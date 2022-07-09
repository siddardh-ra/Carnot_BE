from rest_framework.serializers import ModelSerializer
from .models import Project, ProjectProcessedData


class ListProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def to_representation(self, instance):
        return {"name": instance.name,
                "description": instance.description, "plant_size": instance.plant_size,
                "center": instance.center, "city": instance.city, "state": instance.state,
                "country": instance.country, "project_created_date": instance.project_created_date,
                "organization": str(instance.organization), "status": instance.status,
                "zoom_level": instance.zoom_level, "category": instance.category
                }


class ListStatus_Project(ModelSerializer):
    class Meta:
        model = ProjectProcessedData
        fields = "__all__"

    def to_representation(self, instance):
        resp = {"name": instance.project.name,
                "status": instance.status, "date": instance.date
                }
        return resp
