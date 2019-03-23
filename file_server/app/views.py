import datetime
import os
from django.shortcuts import render
from django.views.generic import TemplateView
from app.settings import FILES_PATH


class FileList(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, date=None):
        # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
        files_list = os.listdir(FILES_PATH)
        result = {'files': []}
        if date is None:
            for item in files_list:
                file_info = os.stat(os.path.join(FILES_PATH, item))
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
            return result
        else:
            try:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                date = datetime.datetime.strptime('2019-03-22 13:22:19.453293',
                                                  '%Y-%m-%d %H:%M:%S.%f').date()
            for item in files_list:
                file_info = os.stat(os.path.join(FILES_PATH, item))
                if datetime.datetime.utcfromtimestamp(file_info.st_ctime).date() == date:
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
            return result


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    file_path = os.path.join(FILES_PATH, name)
    with open(file_path, encoding='utf8') as contents:
        file_contents = contents.read()
        return render(
            request,
            'file_content.html',
            context={'file_name': name, 'file_content': file_contents}
        )
