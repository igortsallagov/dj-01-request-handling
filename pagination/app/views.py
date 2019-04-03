import csv
from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, encoding='cp1251') as file_data:
        contents = csv.DictReader(file_data)
        stops_list = list(contents)
        if request.GET.get('page'):
            page_number = int(request.GET.get('page'))
        else:
            page_number = 1
        p = Paginator(stops_list, 10)
        if page_number in range(1, p.num_pages):
            stops_page = p.page(page_number)
        else:
            stops_page = p.page(p.num_pages)
        current_page = stops_page.number
        prev_page_url = f'?page={stops_page.previous_page_number()}' \
            if stops_page.has_previous() else None
        next_page_url = f'?page={stops_page.next_page_number()}' \
            if stops_page.has_next() else None
        return render_to_response('index.html', context={
            'bus_stations': stops_page,
            'current_page': current_page,
            'prev_page_url': prev_page_url,
            'next_page_url': next_page_url,
        })
