from django.shortcuts import render
import os, shutil, requests, subprocess, datetime, json
from werkzeug.utils import secure_filename
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .forms import UploadDocumentForm
from django.core.files.storage import FileSystemStorage
from django import get_version
from django.http import FileResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt


g_number_of_visitor = {'8-30':30}
g_number_of_file = {'8-30':5}
date = str(datetime.date.today().month) + '-' + str(datetime.date.today().day)
# Create your views here.

def index(request):
    global g_number_of_visitor, g_number_of_file,date
    if g_number_of_visitor.get(date): #해당 날짜의 기록이 존재하면
        g_number_of_visitor[date] += 1
    else:
        g_number_of_visitor[date] = 1

    if not g_number_of_file.get(date):
        tmp = list(g_number_of_file.values())
        g_number_of_file[date] = tmp[len(tmp)-1]

    folder = 'media/my_folder/'
    if request.method=='POST' and request.FILES['inputFile']:
        if g_number_of_file.get(date):  # 해당 날짜의 기록이 존재하면
            g_number_of_file[date] += 1
        else:
            if len(g_number_of_file) == 0:
                g_number_of_file[date] = 1
            else:
                temp = list(g_number_of_file.values())
                g_number_of_file[date] = temp[len(temp) - 1] + 1  # 누적

        myfile = request.FILES['inputFile']

        fn_rm = 'media/my_folder/safe-output-compressed.pdf'
        if os.path.isfile(fn_rm):
            os.remove(fn_rm)
            print('existed file is deleted')

        filelist = list()
        mydir = '/tmp/dangerzone-pixel'
        for f in os.listdir(mydir):
            if f.endswith(".height") or f.endswith(".rgb") or f.endswith(".width"):
                filelist.append(f)
        for f in filelist:
            os.remove(os.path.join(mydir, f))

        fs = FileSystemStorage(location=folder)
        fs.save(myfile.name, myfile)
        filename = myfile.name
        print("파일명", filename)
        file_url = fs.url(filename)
        print('file_url: ',file_url)
        path = '/home/ubuntu/hanium-dangerzone-opensource/media/my_folder/'
        uploadpath = " " + path + filename + " "
        virustotal_resource_id = virustotal_upload(uploadpath)
        subprocess.call(["/usr/bin/dangerzone-container" " documenttopixels --document-filename" + uploadpath + "--pixel-dir /tmp/dangerzone-pixel --container-name flmcode/dangerzone"],shell=True)
        subprocess.call(["/usr/bin/dangerzone-container" " pixelstopdf --pixel-dir /tmp/dangerzone-pixel --safe-dir /tmp/dangerzone-safe --container-name flmcode/dangerzone --ocr 0 --ocr-lang eng"],shell=True)
        #os.rename("/tmp/dangerzone-safe/safe-output-compressed.pdf",
                  # "/tmp/dangerzone-safe/" + filename + "_" + "safe-output.pdf")
        file_url = '/tmp/dangerzone-safe/safe-output-compressed.pdf'
        dest_url = path + 'safe-output-compressed.pdf'
        shutil.move(file_url, dest_url)
        rm_file = 'media/my_folder/'+filename
        if os.path.isfile(rm_file):
            os.remove(rm_file)
            print(rm_file,"is deleted")
        # return render(request, 'fileupload.html', {'file_url': file_url})
        fn = 'safe-output-compressed.pdf'
        jn = 'virustotal-output.json'
        return virustotal_download(virustotal_resource_id,jn)
        # return pdf_view(request,fn)
    else:
        return render(request, 'index.html')

def pdf_view(request, fn):
    fs = FileSystemStorage()
    filename = 'my_folder/' + fn
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="safe.pdf"'
            return response
    else:
        return HttpResponseNotFound('Not Found!!!')
    
def virustotal_upload(orgfile):
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': '4fa229bcb533fedf00e80a7a8023da8fa6f8a2be56d574aceacb8ac3671ddf36'}
    files = {'file': "'" + orgfile + "'"}
    response = requests.post(url, files=files, params=params)
    return response.json()['resource']

def virustotal_download(resource_id, jn):
    fs = FileSystemStorage()
    filename = 'my_folder/' + jn
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': '4fa229bcb533fedf00e80a7a8023da8fa6f8a2be56d574aceacb8ac3671ddf36', 'resource': resource_id}
    response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
    
    if fs.exists(filename):
        
        with fs.open(filename, 'w') as json_file:
            json.dump(response.json(), json_file, indent = 4, sort_keys=True)
            response = HttpResponse(json_file, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="virustotal.json"'
            return response
    else:
        return HttpResponseNotFound('Not Found!!!')



@csrf_exempt
def contact(request):
    return render(request, 'contact.html')

def dashboard(request):
    total_num_of_visitor_label = list(g_number_of_visitor.keys())
    total_num_of_file_label = list(g_number_of_file.keys())
    total_num_of_visitor = list(g_number_of_visitor.values())
    total_num_of_file = list(g_number_of_file.values())
    print(total_num_of_file,total_num_of_visitor)
    return render(request, 'dashboard.html',{'cnt':g_number_of_visitor[date],
                                             'file_cnt': g_number_of_file[date],
                                             'visitor_data':total_num_of_visitor,
                                             'file_data':total_num_of_file,
                                             'visitor_label': total_num_of_visitor_label,
                                             'file_label': total_num_of_file_label
                                             } )

def fileupload(request):
    return render(request,'fileupload.html')

@csrf_exempt
def sendmail(request):
    return render(request,'sendmail.html')


# def fileupload(request):
#     if request.method == 'POST':
#         f = request.files['file']
#         # 저장할 경로 + 파일명
#         filename = f.filename
#         print(filename)
#         path = '/tmp/'
#         f.save(path + secure_filename(filename))
#         uploadpath = " " + path + filename + " "
#         subprocess.call(["/usr/bin/dangerzone-container" " documenttopixels --document-filename" + uploadpath + "--pixel-dir /tmp/dangerzone-pixel --container-name flmcode/dangerzone"],shell=True)
#         subprocess.call(["/usr/bin/dangerzone-container" " pixelstopdf --pixel-dir /tmp/dangerzone-pixel --safe-dir /tmp/dangerzone-safe --container-name flmcode/dangerzone --ocr 0 --ocr-lang eng"],shell=True)
#         os.rename("/tmp/dangerzone-safe/safe-output-compressed.pdf",
#                   "/tmp/dangerzone-safe/" + filename + "_" + "safe-output.pdf")
#         sendfile(request, "/tmp/dangerzone-safe/" + filename + "_" + "safe-output.pdf", mimetype='application/pdf')
#         return "undone"
#     else:
#         return render(request,'fileupload.html')


