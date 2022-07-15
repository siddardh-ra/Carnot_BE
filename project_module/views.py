from json import dumps, loads
from django.contrib.auth.models import Group, User
from django.db.models import Q
from pandas import read_csv
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes)
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from Users.models import UserProfile
from .models import Project, ProjectData, ProjectProcessedData
from .ProjectSerializer import *


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def create(request):
    try:
        data = request.data
        try:
            project = Project()
            project.name = data['name']
            project.plant_size = data['plant_size']
            project.description = data['description']
            project.city = data['city']
            project.state = data['state']
            project.country = data['country']
            project.plant_capacity = data['plant_capacity']
            project.module_type = data['Module']
            project.table_type = data['table']
            project.inverter_type = data['inverter']
            project.project_created_date = data['date']
            try:
                userProfile = UserProfile.objects.get(user=request.user)
                user_group = list(
                    request.user.groups.values_list('name', flat=True))
                project.organization = Group.objects.get(name=user_group[0])
                project.creator = userProfile
            except Exception as e:
                return Response({"status": "failed", "Exception": str(e)})

            project.save()
            proj_name = Project.objects.get(name=data['name'])
            new_ProcessedData = ProjectProcessedData()
            new_ProcessedData.project = proj_name
            new_ProcessedData.date = data['date']
            new_ProcessedData.plant_size_scanned = data['plant_capacity']
            new_ProcessedData.status = "created"
            new_ProcessedData.save()
            flight_summ(request, data['name'], data['date'])
            # trigger_email(request,"Successfully created project "+data['name'],"Project Creation Status")
            return Response({"status": "success"})
        # trigger_email(request, "Failed to create project", "Project Creation Status")
        except Exception as e:
            return Response({"status": "failed", "Exception": str(e)})
    except Exception as e:
        # trigger_email(request, "Failed to create project", "Project Creation Status")
        return Response({"status": "failed", "Exception": str(e)})


def flight_summ(request, p_name, date):
    try:
        proj_name = Project.objects.get(name=p_name)
        evn_data = ProjectData()
        evn_data.project = proj_name
        evn_data.date = date
        evn_data.save()
        return Response({"status": "success"})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def add_date(request, p_name, date):
    try:
        proj_name = Project.objects.get(name=p_name)
        evn_data = ProjectData()
        evn_data.project = proj_name
        evn_data.date = date
        evn_data.save()
        return Response({"status": "success"})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def save_environment_details(request, p_name, date):
    try:
        proj_name = Project.objects.get(name=p_name)
        evn_data = ProjectData.objects.filter(project=proj_name)
        for k in evn_data:
            temp = loads(k.environmental_condition)
            temp[date] = request.data
            k.environmental_condition = dumps(temp)
            k.save()
        return Response({"status": "success"})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def save_payload_details(request, p_name, date):
    try:
        proj_name = Project.objects.get(name=p_name)
        pay_data = ProjectData.objects.filter(project=proj_name)
        for k in pay_data:
            temp = loads(k.payload_check)
            temp[date] = request.data
            k.payload_check = dumps(temp)
            k.save()
        return Response({"status": "success"})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})


class ProjectListApiView(ListAPIView):
    serializer_class = ListProjectSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        try:
            user = self.request.user
            user_group = list(user.groups.values_list('name', flat=True))
            org = Group.objects.get(name=user_group[0])
            return Project.objects.filter(Q(organization=org) | Q(clients=org))
        except Exception as e:
            return Project.objects.none()


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def get_project(request, name):
    project_name = Project.objects.get(name=name)
    try:
        user_group = list(request.user.groups.values_list('name', flat=True))
        company = Group.objects.get(name=user_group[0])
        sub_group = ProjectData.objects.filter(project=project_name)
        temp = {}
        for k in sub_group:
            temp[str(k.date)] = {}
            env = loads(k.environmental_condition)
            pay = loads(k.payload_check)
            temp[str(k.date)]['environment'] = env
            temp[str(k.date)]['payload'] = pay

        resp = {
            "name": project_name.name,
            "description": project_name.name,
            "city": project_name.city,
            "state": project_name.state,
            "country": project_name.country,
            "plant_size": project_name.plant_size,
            "date": project_name.project_created_date,
            "center": project_name.center,
            "organization": str(company),
            "sub-group": temp
        }
        return Response({name: resp})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})@api_view(['GET'])


@api_view(["POST"])
def dump_summary_data(request, project_name):
    data = request.data
    try:
        d = {}
        file = None
        for f in request.FILES:
            file = request.FILES[f]
        date = data.get('date')
        df = read_csv(file)
        p = Project.objects.get(name=project_name)
        projects = ProjectProcessedData()
        projects.project = p
        projects.date = date
        for i in range(len(df)):
            if (df.iloc[i]["criticality"] == "total"):
                d[df.iloc[i]["defect_type"]] = {}
                d[df.iloc[i]["defect_type"]]["defect_type"] = df.iloc[i]["defect_type"]
                d[df.iloc[i]["defect_type"]]["Count"] = int(
                    df.iloc[i]["Count"])
                d[df.iloc[i]["defect_type"]]["kml"] = df.iloc[i]["kml"]
                d[df.iloc[i]["defect_type"]]["color"] = df.iloc[i]["color"]
                d[df.iloc[i]["defect_type"]]["sub_group"] = {}
            else:
                try:
                    d[df.iloc[i]["defect_type"]
                      ]["sub_group"][df.iloc[i]["criticality"]] = {}
                    d[df.iloc[i]["defect_type"]]["sub_group"][df.iloc[i]
                                                              ["criticality"]]["defect_type"] = df.iloc[i]["defect_type"]
                    d[df.iloc[i]["defect_type"]]["sub_group"][df.iloc[i]
                                                              ["criticality"]]["criticality"] = df.iloc[i]["criticality"]
                    d[df.iloc[i]["defect_type"]]["sub_group"][df.iloc[i]
                                                              ["criticality"]]["Count"] = int(df.iloc[i]["Count"])
                    d[df.iloc[i]["defect_type"]]["sub_group"][df.iloc[i]
                                                              ["criticality"]]["kml"] = df.iloc[i]["kml"]
                    d[df.iloc[i]["defect_type"]]["sub_group"][df.iloc[i]
                                                              ["criticality"]]["color"] = df.iloc[i]["color"]
                except KeyError:
                    d[df.iloc[i]["defect_type"]] = {}
                    d[df.iloc[i]["defect_type"]]["sub_group"] = {}
                    d[df.iloc[i]["defect_type"]
                      ]["sub_group"][df.iloc[i]["criticality"]] = {}
                    d[df.iloc[i]["defect_type"]]["sub_group"][df.iloc[i]
                                                              ["criticality"]]["defect_type"] = df.iloc[i]["defect_type"]
                    d[df.iloc[i]["defect_type"]]["sub_group"][df.iloc[i]
                                                              ["criticality"]]["criticality"] = df.iloc[i]["criticality"]
                    d[df.iloc[i]["defect_type"]]["sub_group"][df.iloc[i]
                                                              ["criticality"]]["Count"] = int(df.iloc[i]["Count"])
                    d[df.iloc[i]["defect_type"]]["sub_group"][df.iloc[i]
                                                              ["criticality"]]["kml"] = df.iloc[i]["kml"]
                    d[df.iloc[i]["defect_type"]]["sub_group"][df.iloc[i]
                                                              ["criticality"]]["color"] = df.iloc[i]["color"]
        projects.summary_layers = dumps(d)
        projects.save()
        return Response({"status": "success"})
    except Exception as e:
        return Response({"status": "failed", "exception": str(e)})


@api_view(["POST"])
def dump_inverter_data(request, project_name):
    data = request.data
    try:
        d = {}
        file = None
        for f in request.FILES:
            file = request.FILES[f]
        date = data.get('date')
        df = read_csv(file)
        p = Project.objects.get(name=project_name)
        projects = ProjectProcessedData()
        projects.project = p
        projects.date = date
        for i in range(len(df)):
            try:
                if (df.iloc[i]["sub_class"] == "total"):
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]] = {}
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]
                                              ]["count"] = str(df.iloc[i]["Count"])
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]
                                              ]["kml"] = df.iloc[i]["kml_name"]
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]
                                              ]["color"] = str(df.iloc[i]["color_code"])
                    d[df.iloc[i]["block_id"]][df.iloc[i]
                                              ["subgroup"]]["sub_group"] = {}
                else:
                    try:
                        d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]
                                                  ]["sub_group"][df.iloc[i]["sub_class"]] = {}
                    except KeyError:
                        d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]] = {}
                        d[df.iloc[i]["block_id"]][df.iloc[i]
                                                  ["subgroup"]]["sub_group"] = {}
                        d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]
                                                  ]["sub_group"][df.iloc[i]["sub_class"]] = {}
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]]["sub_group"][df.iloc[i]
                                                                                   ["sub_class"]]["sub_class"] = df.iloc[i]["sub_class"]
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]]["sub_group"][df.iloc[i]
                                                                                   ["sub_class"]]["count"] = str(df.iloc[i]["Count"])
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]
                                              ]["sub_group"][df.iloc[i]["sub_class"]]["kml"] = df.iloc[i]["kml_name"]
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]]["sub_group"][df.iloc[i]
                                                                                   ["sub_class"]]["color"] = str(df.iloc[i]["color_code"])
            except KeyError:
                if (df.iloc[i]["sub_class"] == "total"):
                    d[df.iloc[i]["block_id"]] = {}
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]] = {}
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]
                                              ]["count"] = str(df.iloc[i]["Count"])
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]
                                              ]["kml"] = df.iloc[i]["kml_name"]
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]
                                              ]["color"] = str(df.iloc[i]["color_code"])
                    d[df.iloc[i]["block_id"]][df.iloc[i]
                                              ["subgroup"]]["sub_group"] = {}
                else:
                    try:
                        d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]
                                                  ]["sub_group"][df.iloc[i]["sub_class"]] = {}
                    except KeyError:
                        d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]] = {}
                        d[df.iloc[i]["block_id"]][df.iloc[i]
                                                  ["subgroup"]]["sub_group"] = {}
                        d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]
                                                  ]["sub_group"][df.iloc[i]["sub_class"]] = {}
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]]["sub_group"][df.iloc[i]
                                                                                   ["sub_class"]]["sub_class"] = df.iloc[i]["sub_class"]
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]]["sub_group"][df.iloc[i]
                                                                                   ["sub_class"]]["count"] = str(df.iloc[i]["Count"])
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]
                                              ]["sub_group"][df.iloc[i]["sub_class"]]["kml"] = df.iloc[i]["kml_name"]
                    d[df.iloc[i]["block_id"]][df.iloc[i]["subgroup"]]["sub_group"][df.iloc[i]
                                                                                   ["sub_class"]]["color"] = str(df.iloc[i]["color_code"])
        projects.inverter_layers = dumps(d)
        projects.save()
        return Response({"status": "success"})
    except Exception as e:
        return Response({"status": "failed", "exception": str(e)})


@api_view(["GET"])
def retrieve_summary_data(request, project_name):
    try:
        resp = {}
        temp = Project.objects.get(name=project_name)
        projects = ProjectProcessedData.objects.filter(project=temp)
        for project in projects:
            project_id = project.project.id
            try:
                resp[project_id]['name'] = project.project.name
                resp[project_id]['dates'].append(str(project.date))
                resp[project_id]['location'] = str(project.project.state)
                resp[project_id]['plant_size'] = str(
                    project.project.plant_size)
            except Exception as e:
                resp[project_id] = {}
                resp[project_id]['project_id'] = project_id
                resp[project_id]['name'] = project.project.name
                resp[project_id]['dates'] = []
                resp[project_id]['dates'].append(str(project.date))
                resp[project_id]['location'] = str(project.project.state)
                resp[project_id]['plant_size'] = str(
                    project.project.plant_size)
            date = str(project.date)
            resp[project_id][date] = {}
            layers = loads(project.summary_layers)
            resp[project_id][date]["summary_data"] = layers
        return Response(resp)
    except Exception as e:
        return Response(resp)


@api_view(["GET"])
def retrieve_inverter_data(request, project_name):
    try:
        resp = {}
        temp = Project.objects.get(name=project_name)
        projects = ProjectProcessedData.objects.filter(project=temp)
        for project in projects:
            project_id = project.project.id
            try:
                resp[project_id]['name'] = project.project.name
                resp[project_id]['dates'].append(str(project.date))
                resp[project_id]['location'] = str(project.project.state)
                resp[project_id]['plant_size'] = str(
                    project.project.plant_size)
            except Exception as e:
                resp[project_id] = {}
                resp[project_id]['project_id'] = project_id
                resp[project_id]['name'] = project.project.name
                resp[project_id]['dates'] = []
                resp[project_id]['dates'].append(str(project.date))
                resp[project_id]['location'] = str(project.project.state)
                resp[project_id]['plant_size'] = str(
                    project.project.plant_size)
            date = str(project.date)
            resp[project_id][date] = {}
            layers = loads(project.inverter_layers)
            resp[project_id][date]["inverter_data"] = layers
        return Response(resp)
    except Exception as e:
        return Response(resp)


@api_view(["GET"])
def get_project_data_by_date(request, project, date):
    try:
        resp = {}
        temp = Project.objects.get(name=project)
        projects = ProjectProcessedData.objects.filter(
            project=temp).filter(date=date)
        for project in projects:
            if str(project.date) == date:
                project_id = project.project.id
                try:
                    resp[project_id]['name'] = project.project.name
                    resp[project_id]['dates'].append(str(project.date))
                    resp[project_id]['location'] = str(project.project.state)
                    resp[project_id]['plant_size'] = str(
                        project.project.plant_size)
                except Exception as e:
                    resp[project_id] = {}
                    resp[project_id]['project_id'] = project_id
                    resp[project_id]['name'] = project.project.name
                    resp[project_id]['dates'] = []
                    resp[project_id]['dates'].append(str(project.date))
                    resp[project_id]['location'] = str(project.project.state)
                    resp[project_id]['plant_size'] = str(
                        project.project.plant_size)
                date = str(project.date)
                resp[project_id][date] = {}
                summary_data = loads(project.summary_layers)
                resp[project_id][date]["summary_data"] = summary_data
                inverter_data = loads(project.inverter_layers)
                resp[project_id][date]["inverter_data"] = inverter_data
        return Response(resp)
    except Exception as e:
        return Response({"status": "failure", "exception": str(e)})


@api_view(["GET"])
def retrieve_project_data(request, project):
    try:
        resp = {}
        temp = Project.objects.get(name=project)
        projects = ProjectProcessedData.objects.filter(project=temp)
        strore_temp_status = {}
        for project in projects:
            total_temp_dash = {}
            project_id = project.project.id
            try:
                resp[project_id]['name'] = project.project.name
                resp[project_id]['dates'].append(str(project.date))
                resp[project_id]['location'] = str(project.project.state)
                resp[project_id]['plant_size'] = str(
                    project.project.plant_size)
                resp[project_id]['plant_capacity'] = str(
                    project.project.plant_capacity)
                resp[project_id]['center'] = str(project.project.center)
                resp[project_id]['category'] = str(project.project.category)
                resp[project_id]['zoom_level'] = str(
                    project.project.zoom_level)
                strore_temp_status[str(project.date)] = project.status
                resp[project_id]['date_status'] = strore_temp_status
            except Exception as e:
                resp[project_id] = {}
                resp[project_id]['project_id'] = project_id
                resp[project_id]['name'] = project.project.name
                resp[project_id]['dates'] = []
                resp[project_id]['dates'].append(str(project.date))
                resp[project_id]['location'] = str(project.project.state)
                resp[project_id]['plant_size'] = str(
                    project.project.plant_size)
                resp[project_id]['plant_capacity'] = str(
                    project.project.plant_capacity)
                resp[project_id]['center'] = str(project.project.center)
                resp[project_id]['category'] = str(project.project.category)
                resp[project_id]['zoom_level'] = str(
                    project.project.zoom_level)
                strore_temp_status[str(project.date)] = project.status
                resp[project_id]['date_status'] = strore_temp_status
            date = str(project.date)
            resp[project_id][date] = {}
            resp[project_id][date]["summary_data"] = loads(
                project.summary_layers)
            resp[project_id][date]["inverter_data"] = loads(
                project.inverter_layers)
            resp[project_id][date]["power_loss"] = loads(project.power_loss)
            resp[project_id][date]["topography_data"] = loads(
                project.topography_layers)
            resp[project_id][date]["grading_layers"] = loads(
                project.grading_layers)
            resp[project_id][date]["ortho_file_location"] = project.ortho_file_location
            resp[project_id][date]["kml_file_location"] = project.kml_file_location
            resp[project_id][date]["report_path"] = project.report_path
            resp[project_id][date]["thermal_location"] = project.thermal_hotspot_location
            resp[project_id][date]["cad_file_location"] = project.cad_file_location
            resp[project_id][date]["dtm_legend"] = project.dtm_legend
            resp[project_id][date]["slope_legend"] = project.slope_legend
            resp[project_id][date]["csv_path"] = project.csv_path
            resp[project_id][date]["total_power_loss"] = project.total_power_loss
            resp[project_id][date]["total_modules_present"] = project.total_modules_present
            load_summ = loads(project.summary_layers)
            if not load_summ == {}:
                for i in load_summ:
                    if load_summ[i]["sub_group"] == {}:
                        total_temp_dash[i] = load_summ[i]["Count"]
                    else:
                        temp_subgroup = load_summ[i]["sub_group"]
                        for kl in temp_subgroup:
                            if kl == "Others":
                                total_temp_dash["Hotspot"] = temp_subgroup[kl]["Count"]
                            elif kl == "Table" or kl == "Module":
                                total_temp_dash[str(
                                    kl)+" Failure"] = temp_subgroup[kl]["Count"]
                            else:
                                total_temp_dash[kl] = temp_subgroup[kl]["Count"]
            resp[project_id][date]["health_history"] = total_temp_dash
            resp[project_id][date]["total_no_defects"] = sum(
                total_temp_dash.values())
        return Response(resp)
    except Exception as e:
        return Response({"status": "failure", "exception": str(e)})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def get_projects_status(request):
    try:
        userProfile = UserProfile.objects.get(user=request.user)
        get_user = User.objects.get(username=request.user)
        test = Project.objects.filter(
            Q(creator=userProfile) | Q(shared_profile=get_user))
        temp = {}
        for i in test:
            sub_group = ProjectProcessedData.objects.filter(project=i)
            strore_temp_status = {}
            for k in sub_group:
                temp_list = list(k.project.shared_profile.all())
                temp_arr = [{"name": character.get_full_name(), "email": character.email}
                            for character in temp_list if character.email != "info@datasee.ai"]
                try:
                    strore_temp_status[str(k.date)] = k.status
                    temp[str(k.project.name)]['name'] = i.name
                    temp[str(k.project.name)]['id'] = k.project.id
                    temp[str(k.project.name)
                         ]['plant_size'] = k.project.plant_size
                    temp[str(k.project.name)
                         ]['plant_capacity'] = k.project.plant_capacity
                    temp[str(k.project.name)]['category'] = k.project.category
                    temp[str(k.project.name)]['center'] = k.project.center
                    temp[str(k.project.name)
                         ]['zoom_level'] = k.project.zoom_level
                    temp[str(k.project.name)]['city'] = k.project.city
                    temp[str(k.project.name)]['state'] = k.project.state
                    temp[str(k.project.name)]['country'] = k.project.country
                    temp[str(k.project.name)]['status'] = strore_temp_status
                    temp[str(k.project.name)]['report_path'] = k.report_path
                    temp[str(k.project.name)]['shared'] = {
                        "created_by": k.project.creator.user.email, "shared_to": temp_arr}
                except Exception as e:
                    temp[str(k.project.name)] = {}
                    strore_temp_status[str(k.date)] = k.status
                    temp[str(k.project.name)]['name'] = i.name
                    temp[str(k.project.name)]['id'] = k.project.id
                    temp[str(k.project.name)
                         ]['plant_size'] = k.project.plant_size
                    temp[str(k.project.name)
                         ]['plant_capacity'] = k.project.plant_capacity
                    temp[str(k.project.name)]['center'] = k.project.center
                    temp[str(k.project.name)]['category'] = k.project.category
                    temp[str(k.project.name)
                         ]['zoom_level'] = k.project.zoom_level
                    temp[str(k.project.name)]['city'] = k.project.city
                    temp[str(k.project.name)]['state'] = k.project.state
                    temp[str(k.project.name)]['country'] = k.project.country
                    temp[str(k.project.name)]['status'] = strore_temp_status
                    temp[str(k.project.name)]['report_path'] = k.report_path
                    temp[str(k.project.name)]['shared'] = {
                        "created_by": k.project.creator.user.email, "shared_to": temp_arr}
        return Response(temp)
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def Recent_project_List(request):
    try:
        userProfile = UserProfile.objects.get(user=request.user)
        get_user = User.objects.get(username=request.user)
        sub_group = ProjectProcessedData.objects.filter(Q(project__creator=userProfile) | Q(
            project__shared_profile=get_user)).distinct().order_by('-date')[:3]
        t_list = []
        for k in sub_group:
            temp = {}
            temp['name'] = k.project.name
            temp['plant_size'] = k.project.plant_size
            temp['plant_capacity'] = k.project.plant_capacity
            temp['center'] = k.project.center
            temp['city'] = k.project.city
            temp['state'] = k.project.state
            temp['country'] = k.project.country
            temp['date'] = k.date
            temp['status'] = k.status
            t_list.append(temp)
        return Response(t_list)
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def add_new_date(request, p_name, date):
    try:
        proj_name = Project.objects.get(name=p_name)
        new_ProcessedData = ProjectProcessedData()
        new_ProcessedData.project = proj_name
        new_ProcessedData.date = date
        new_ProcessedData.plant_size_scanned = proj_name.plant_capacity
        new_ProcessedData.status = "created"
        new_ProcessedData.save()
        return Response({"status": "success"})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def get_dashboard_data(request):
    try:
        userProfile = UserProfile.objects.get(user=request.user)
        get_user = User.objects.get(username=request.user)
        sub_group = ProjectProcessedData.objects.filter(
            Q(project__creator=userProfile) | Q(project__shared_profile=get_user)).distinct()
        total_temp_dash = {}
        plant_size_scanned = 0
        total_power_loss = 0
        total_defects = 0
        for k in sub_group:
            plant_size_scanned = plant_size_scanned + \
                float(k.plant_size_scanned)
            total_power_loss = total_power_loss + float(k.total_power_loss)
            total_defects = total_defects + float(k.total_defects)
            load_summ = loads(k.summary_layers)
            if not load_summ == {}:
                for i in load_summ:
                    if i in total_temp_dash:
                        total_temp_dash[i] = total_temp_dash[i] + \
                            load_summ[i]["Count"]
                    else:
                        total_temp_dash[i] = load_summ[i]["Count"]
        return Response({"dashboard_total": total_temp_dash, "plant_size_scanned": format(
            plant_size_scanned, '.2f'), "total_power_loss": format(total_power_loss, '.2f'), "total_defects": sum(total_temp_dash.values())})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def share_project(request, id):
    data = request.data
    email_id = data["email_id"]
    temp = Project.objects.get(id=id)
    try:
        temp_list = list(temp.shared_profile.all())
        if len(temp_list) >= 3:
            return Response({"status": "failed", "Notification": "Sharing limit exceeded. Contact administrator for further details"})
        get_user = User.objects.get(email=email_id)
        temp.shared_profile.add(get_user)
        temp.save()
        temp_list = list(temp.shared_profile.all())
        temp_arr = [{"name": character.get_full_name(), "email": character.email}
                    for character in temp_list if character.email != "info@datasee.ai"]
        return Response({"status": "success", "revised_data": {"created_by": temp.creator.user.email, "shared_to": temp_arr}})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e), "Notification": "No user with the requested e-mail. Kindly notify the user to signup and request again. "})


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def update(request):
    try:
        Project.objects.all().update(zoom_level="15", category="thermography")
        return Response({"status": "success"})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})
