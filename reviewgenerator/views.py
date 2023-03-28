from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def frontpage(request):
    print(request.POST)
    if 'user_input' in request.POST:
        user_input = request.POST['user_input']
        return render(request, 'reviewgenerator/frontpage.html', {'user_input': user_input})
    else:
        return render(request, 'reviewgenerator/frontpage.html')


def my_js_test(request):
    print("get ajax request")
    print(request)
    data = {
        'content': 'Updated content'
    }

    return JsonResponse(data)


def my_js_view(request):
    return render(request, 'reviewgenerator/ajaxtest.html')
