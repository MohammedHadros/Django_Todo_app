from django.shortcuts import render

def custom_page_not_found(request, exception):
    return render(request, "not-found.html", status=404)


def handel_server_error(request):
    return render(request,"server-error.html")

