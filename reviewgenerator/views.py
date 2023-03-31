import json

from django.shortcuts import render
from django.http import JsonResponse

from decouple import config

import openai


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
    # print(request)
    # print(request.body)
    request_data = json.loads(request.body)
    # print(request_data)
    # print(request_data.get('inputReview'))

    # my_content = "test"

    input_review = request_data.get('inputReview')

    openai.api_key = config('openai_key')

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Please rewrite this customer review with more details: " + input_review},
        ]
    )

    my_content = response['choices'][0]['message']['content']

    print(input_review)
    print(my_content)

    data = {
        'content': my_content
    }

    return JsonResponse(data)


def my_js_view(request):
    return render(request, 'reviewgenerator/ajaxtest.html')
