from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import SearchedPhrase
from bs4 import BeautifulSoup
import requests
from serpapi import GoogleSearch
import json


# Create your views here.

def index(request):
    # Zachycení metody POST a hledaného výrazu
    if request.method == "POST":
        form = SearchedPhrase(request.POST)
        # Validace formuláře pomocí Djanga
        if form.is_valid():
            # Data z formuláře se odešlou do metody která pomocí API zjistí vyhledávání
            data = find_soup_with_api(form.cleaned_data)
            return save_json(data)

    form = SearchedPhrase()
    return render(request, "prakticka_cast/index.html",{
                  "search_form": form
                  })

# Metoda, která dostane data a uloží je do souboru results.json
def save_json(data):
    if isinstance(data, str):
        try:
            parsed_data = json.loads(data)
        except json.JSONDecodeError:
            parsed_data = data
    else:
        parsed_data = data

    response = HttpResponse(
        json.dumps(parsed_data, indent=4, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )
    response["Content-Disposition"] = 'attachment; filename="results.json"'

    return response

# Serpapi vyhledávání
def find_soup_with_api(data):
    params = {
        "q": data["input_text"],
        "location": "Prague, Czechia",
        "hl": "cs",
        "gl": "cz",
        "google_domain": "google.cz",
        "api_key": "ac40968211c36a3cbd5e4a4cfce02b1df1856d6b5a6afce4cc9d096efa572c53",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    organic = results.get("organic_results", [])

    return organic