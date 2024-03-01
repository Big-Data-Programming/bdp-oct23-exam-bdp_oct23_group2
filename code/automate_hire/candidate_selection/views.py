from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import asyncio

from .services.data_insertion import insert_data, insert_stackoverflow_data


def fetch_data(request):
    """
    Fetch data from GitHub and insert it into the database.
    """
    asyncio.run(insert_data())
    
    return HttpResponse('Data fetched and inserted successfully!')

def fetch_stackoverflow_data(request):
    
    insert_stackoverflow_data()
    
    return HttpResponse('Stackoverflow Data fetched successfully!')
