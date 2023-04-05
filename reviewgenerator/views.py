import json

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from .models import GptHistory

from decouple import config

import openai


# Create your views here.
# 暂时没用的view
def frontpage(request):
    print(request.POST)
    if 'user_input' in request.POST:
        user_input = request.POST['user_input']
        return render(request, 'reviewgenerator/frontpage.html', {'user_input': user_input})
    else:
        return render(request, 'reviewgenerator/frontpage.html')


# 读js请求 返回gpt response
def my_js_test(request):
    print("get js request")
    # print(request)
    # print(request.body)
    request_data = json.loads(request.body)
    # print(request_data)
    # print(request_data.get('inputReview'))

    # my_content = "test"

    # get textarea input
    input_review = request_data.get('inputReview')

    # get selected language
    selected_language = request_data.get('selectedLanguage')
    print(selected_language)

    # get selected application
    selected_application = request_data.get('selectedApplication')
    print(selected_application)

    # get selected rate
    selected_rate = request_data.get('selectedRate')
    print(selected_rate)

    # get selected keywords
    selected_keywords = request_data.get('selectedKeyWords')
    print(selected_keywords)

    # send request to chatgpt
    # openai.api_key = config('openai_key')
    #
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "user", "content": "Please rewrite this customer review with more details: " + input_review},
    #     ]
    # )
    #
    # my_content = response['choices'][0]['message']['content']
    #
    # print(input_review)
    # print(my_content)
    #
    # data = {
    #     'content': my_content
    # }

    # insert into database
    gpt_history = GptHistory(pub_date=timezone.now(),
                             textarea_input=input_review,
                             prompt_used="example",
                             language_used=selected_language,
                             pic_name=None,
                             generated_gpt="example",
                             star_rating=int(selected_rate),
                             keywords=",".join(selected_keywords),
                             )

    gpt_history.save()

    data = {
        "inputReview":
            input_review,
        "selectedLanguage":
            selected_language,
        "selectedApplication":
            selected_application,
        "selectedRate":
            selected_rate,
        "selectedKeyWords":
            selected_keywords,
    }

    return JsonResponse(data)


# review generator页面
def my_js_view(request):
    return render(request, 'reviewgenerator/jstest.html')
