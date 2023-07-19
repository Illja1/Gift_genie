from django.shortcuts import render
import asyncio
from django.core.cache import cache
from asgiref.sync import sync_to_async, async_to_sync
from .forms import GiftFinderForm
from django.views.decorators.csrf import csrf_exempt
import openai
import aiohttp
import requests
from django.http import JsonResponse

@csrf_exempt
def gift_finder(request):
    async def inner(request):
        if request.method == 'POST':
            form = GiftFinderForm(request.POST)
            if form.is_valid():
                age = form.cleaned_data['age']
                gender = form.cleaned_data['gender']
                interests = form.cleaned_data['interests']

                # Authenticate with OpenAI API
                openai.api_key = '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'

                # Generate gift list using ChatGPT
                prompt = f"Find gifts for {gender} person, {age} years old, with interests in {interests}."
                response = await asyncio.to_thread(openai.Completion.create,
                                                   engine="text-curie-001",
                                                   prompt=prompt,
                                                   max_tokens=60,
                                                   n=1,
                                                   stop=None,
                                                   temperature=0.5,
                                                   )
                gifts = response.choices[0].text.strip()

                # Make a request to the AliExpress API
                url = 'https://api.aliexpress.com/search'
                params = {
                    'apiKey': 'YOUR_ALIEXPRESS_API_KEY',
                    'currency': 'USD',
                    'sort': 'price_asc',
                    'keywords': gifts,
                }
                response = requests.get(url, params=params)
                results = response.json()

                
                cache_key = f"gift_finder_{gender}_{age}_{interests}"
                cache.set(cache_key, (results, gifts), timeout=3600)

               
                return JsonResponse({'gifts': gifts})

        else:
            form = GiftFinderForm()
            rendered = await sync_to_async(render)(request, 'gift/gift_finder.html', {'form': form})
            return rendered

    return async_to_sync(inner)(request)


def  index(request):
    return render(request,'gift/index.html')

# @csrf_exempt
# def gift_finder(request):
#     async def inner(request):
#         if request.method == 'POST':
#             form = GiftFinderForm(request.POST)
#             if form.is_valid():
#                 age = form.cleaned_data['age']
#                 gender = form.cleaned_data['gender']
#                 interests = form.cleaned_data['interests']
#
#                 # Authenticate with OpenAI API
#                 openai.api_key = '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'
#
#                 # Generate gift list using ChatGPT
#                 prompt = f"Find gifts for {gender} person, {age} years old, with interests in {interests}."
#                 response = await asyncio.to_thread(openai.Completion.create,
#                                                    engine="text-curie-001",
#                                                    prompt=prompt,
#                                                    max_tokens=60,
#                                                    n=1,
#                                                    stop=None,
#                                                    temperature=0.5,
#                                                    )
#                 gifts = response.choices[0].text.strip()
#
#                 # Return the generated gifts as the response
#                 return JsonResponse({'gifts': gifts})
#
#         else:
#             form = GiftFinderForm()
#             rendered = await sync_to_async(render)(request, 'gift/gift_finder.html', {'form': form})
#             return rendered
#
#     return async_to_sync(inner)(request)









#'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'
#'7C81F6D0D7724B06BA9068CE9D045D14'