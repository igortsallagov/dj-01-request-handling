import csv
from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, encoding='cp1251') as file_data:
        contents = csv.DictReader(file_data)
        stops_list = list(contents)
        page_number = request.GET.get('page')
        p = Paginator(stops_list, 10)
        try:
            stops_page = p.page(page_number)
        except PageNotAnInteger:
            stops_page = p.page(1)
        except EmptyPage:
            stops_page = p.page(p.num_pages)
        current_page = stops_page.number
        if current_page == 1:
            prev_page_url = None
        else:
            prev_page_url = f'?page={stops_page.previous_page_number()}'
        try:
            next_page_url = f'?page={stops_page.next_page_number()}'
        except EmptyPage:
            next_page_url = None
        return render_to_response('index.html', context={
            'bus_stations': stops_page,
            'current_page': current_page,
            'prev_page_url': prev_page_url,
            'next_page_url': next_page_url,
        })
