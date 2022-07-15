from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Users.models import *
from .models import UploaderLog
from project_module.models import Project
from os import mkdir, makedirs
from json import loads, dumps


uploadpath = "/assets/"


@csrf_exempt
def upload(request, project_name):
    str(request.POST.get('flowChunkNumber'))
    flowChunkSize = str(request.POST.get('flowCurrentChunkSize'))
    flowFileName = request.POST.get('flowFilename')
    str(request.POST.get('flowTotalSize'))
    str(request.POST.get('flowTotalChunks'))
    flowRelativePath = str(request.POST.get('flowRelativePath'))
    try:
        file = request.FILES['file'].read()
    except Exception as e:
        return JsonResponse(data={"status": "failed"}, safe=False)
    try:
        project = project_name
    except Exception as e:
        project = ""
    try:
        mkdir(uploadpath)
    except Exception as e:
        print("Exception is e ", e)
    dirs = flowRelativePath.split("/")
    del dirs[-1]
    path = path.join(uploadpath, *dirs)
    try:
        makedirs(path)
    except Exception as e:
        print("Exception is e ", str(e))
    try:
        i = 0
        flag = True
        while i <= 5 and flag:
            flag = retry(path+"/"+flowFileName, file, flowChunkSize)
            i = i+1

        if path.exists(path+"/"+flowFileName):
            temp = loads(upload.filesuploaded)
            temp[flowRelativePath] = flowFileName
            # upload.filesuploaded=dumps((temp))
            # upload.save()
            from time import sleep
            sleep(1.0)
        else:
            print("Path doesnt exist ", path+"/"+flowFileName)
    except Exception as e:
        print("Exception occured is ", e)
    return JsonResponse(data={"status": "success"}, safe=False)


def retry(path, file, flowChunkSize):
    try:
        if not path.exists(path):
            with open(path, "wb") as out:
                out.write(file)
        elif not str(path.getsize(path)) == str(flowChunkSize):
            with open(path, "wb") as out:
                out.write(file)
        else:
            print("File already exixsts")
    except FileExistsError as e:
        print("Exception im ", e)
        return False
    except Exception as e:
        print("Exception is ", e)
        return True
    return False


@csrf_exempt
def store_files_meta_info(request, project_name):
    data = loads(request.body)
    Project_Name = Project.objects.get(name=project_name)
    upload_queryset = list(UploaderLog.objects.filter(project=Project_Name))
    if len(upload_queryset) == 0:
        upload = UploaderLog()
        upload.project = Project_Name
        upload.uploaded_by = request.user.username
        upload.relative_path = uploadpath+project_name
        upload.total_number_of_files = data['total']
        upload.allfiles = dumps(data["allfiles"])
        upload.number_of_files_uploaded = 0
        upload.filesuploaded = "{}"
        upload.save()
    else:
        upload = upload_queryset[0]
        upload.uploaded_by = request.user.username
        upload.relative_path = uploadpath + project_name
        upload.total_number_of_files = data['total']
        upload.number_of_files_uploaded = 0
        upload.allfiles = dumps(data["allfiles"])
        upload.filesuploaded = "{}"
        upload.save()

    return JsonResponse(data={"data": "all ok"}, safe=False)
