from django.shortcuts import render
from django.http import HttpResponse
import openai
from dotenv import load_dotenv
import os

# Create your views here.

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
responses = HttpResponse()

def about(response):
    return render(response, 'aboutUs.html')

def results(response):
    query = responses.get('query')
    print(query)
    p1 = f"Explain  to a non programmer in at least 300 words.{query}"
    p2 = f"Give a roadmap that is a series of instructions that someone should take to solve this question. {query} Number each point"
    
    resp = openai.Completion.create(
        model="text-davinci-002",
        prompt= p1,
        temperature=0.15,
        max_tokens=500,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0.5
    )
    roadmap = openai.Completion.create(
        model="text-davinci-002",
        prompt= p2,
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    resps = {'response': resp["choices"][0]["text"], 'query': query, 'roadmap': roadmap["choices"][0]["text"]}
    return render(response, 'result.html', resps)

def search(response):
    return render(response, 'index.html')

def query(request):
    if request.method == 'POST':
        if 'query' in request.POST:
            q = str(request.POST['query'])
            responses.headers['query'] = q