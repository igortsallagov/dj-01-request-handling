import datetime
import os
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings


class FileList(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, date=None):
        # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
        files_list = os.listdir(settings.FILES_PATH)
        result = {'files': []}
        for item in files_list:
            file_info = os.stat(os.path.join(settings.FILES_PATH, item))
            result['files'].append(
                {
                    'name': item,
                    'ctime': datetime.datetime.utcfromtimestamp(
                        file_info.st_ctime
                    ),
                    'mtime': datetime.datetime.utcfromtimestamp(
                        file_info.st_mtime
                    )
                }
            )
        if date:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            result = {
                'files': [item for item in result['files']
                               if item['ctime'].date() == date],
                'date': date
            }
        return result


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    file_path = os.path.join(settings.FILES_PATH, name)
    if os.path.exists(file_path):
        with open(file_path, encoding='utf8') as contents:
            file_contents = contents.read()
    else:
        file_contents = f'File {name} not found'
    return render(
        request,
        'file_content.html',
        context={'file_name': name, 'file_content': file_contents}
)
