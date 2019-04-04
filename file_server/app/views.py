from datetime import datetime as dt
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponseNotFound
import os


class FileList(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, date=None):
        # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
        files_list = os.listdir(settings.FILES_PATH)
        files_data = list()
        for item in files_list:
            file_info = os.stat(os.path.join(settings.FILES_PATH, item))
            files_data.append(
                {
                    'name': item,
                    'ctime': dt.utcfromtimestamp(
                        file_info.st_ctime
                    ),
                    'mtime': dt.utcfromtimestamp(
                        file_info.st_mtime
                    )
                }
            )
        result = {
            'files': [item for item in files_data if item['ctime'].date()
                      == dt.strptime(date, '%Y-%m-%d').date()] if date else files_data,
            'date': date
        }
        return result


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    file_path = os.path.join(settings.FILES_PATH, name)
    if os.path.exists(file_path):
        with open(file_path, encoding='utf8') as contents:
            file_contents = contents.read()
            return render(
                request,
                'file_content.html',
                context={'file_name': name, 'file_content': file_contents}
            )
    else:
        return HttpResponseNotFound('404. Not found')
