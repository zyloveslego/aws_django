from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

import json

from django.http import JsonResponse
from django.utils import timezone

from .models import GptHistory, UploadPic

import os
import sys
import requests

from django.conf import settings


from django.core.files.base import ContentFile

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


# register
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(data=request.POST)
        # print(request.POST)
        # print("\n")
        # print(form.errors)
        # print("\n")
        # print(form)
        # print("\n")
        # print(form.is_valid())
        if form.is_valid():
            print("get in")
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("reviewgenerator:jsview")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="reviewgenerator/register.html", context={"register_form": form})


# login
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("reviewgenerator:jsview")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="reviewgenerator/login.html", context={"login_form": form})


def object_detect(image):
    MODE = 'demo'

    # Your RapidAPI key. Fill this variable with the proper value if you want
    # to try api4ai via RapidAPI marketplace.
    RAPIDAPI_KEY = ''

    OPTIONS = {
        'demo': {
            'url': 'https://demo.api4ai.cloud/general-det/v1/results',
            'headers': {'A4A-CLIENT-APP-ID': 'sample'}
        },
        'rapidapi': {
            'url': 'https://general-detection.p.rapidapi.com/v1/results',
            'headers': {'X-RapidAPI-Key': RAPIDAPI_KEY}
        }
    }

    if '://' in image:
        # POST image via URL.
        response = requests.post(
            OPTIONS[MODE]['url'],
            headers=OPTIONS[MODE]['headers'],
            data={'url': image})
    else:
        # POST image as file.
        with open(image, 'rb') as image_file:
            response = requests.post(
                OPTIONS[MODE]['url'],
                headers=OPTIONS[MODE]['headers'],
                files={'image': (os.path.basename(image), image_file)}
            )

    # Print raw response.
    # print(f'Raw response:\n{response.text}\n')

    # Parse response and objects with confidence > 0.5.
    confident = [x['entities'][0]['classes']
                 for x in response.json()['results'][0]['entities'][0]['objects']  # noqa
                 if list(x['entities'][0]['classes'].values())[0] > 0.5]

    print(f'{len(confident)} objects found with confidence above 0.5:\n{confident}\n')

    return f'{len(confident)} objects found with confidence above 0.5:\n{confident}\n'

# upload picture
def upload_pic(request):
    if request.method == 'POST':
        pic = request.FILES.get('pic')
        pic_name = request.FILES.get('pic').name
        new_img = UploadPic(
            photo=pic,  # 取到图片
            title=pic_name  # 取到图片的名字
        )
        new_img.save()  # 保存图片

        # 传入object detection
        print(pic_name)
        # print(str(settings.MEDIA_ROOT))
        object_detected = object_detect(str(settings.MEDIA_ROOT) + "/" + pic_name)

        context = {'pic_name': pic_name, 'object_detected': object_detected}
        return render(request, 'reviewgenerator/pic_upload_test.html', context)

    return render(request, 'reviewgenerator/pic_upload_test.html')



