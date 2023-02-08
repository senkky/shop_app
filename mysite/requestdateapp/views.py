from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, "requestdateapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, "requestdateapp/user-bio-form.html")

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.FILES.get('myfile'):
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        if myfile.size > 1048576:
            raise ProcessLookupError('The file size is too large')
        else:
            filename = fs.save(myfile.name, myfile)
            print("saved file", filename)
    return render(request, "requestdateapp/file-upload.html")