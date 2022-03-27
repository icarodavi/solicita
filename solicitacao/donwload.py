from django.http import HttpResponse
from django.urls import reverse_lazy
import re
import os


class DownloadResponse(HttpResponse):
    """
    A download HTTP response class that forces download in the browser or redirects to URL given for file.

    Args:
        request (django.http.HttpRequest): We need this to send a `message.success`
            to client if the report is being generated
            when `path` callable returns `None`
        path (callable or str): A callable object that returns a path
            located in the local file system or a str object with the path
        filename (str): Given to the browser for the downloaded file
        redirect_to (str): Where to redirect the user if `path` callable returns `None`
        * (diverse): All configuration available for Django's HttpResponse class

    Kwargs:
        content_type (str): Tells the browser the type of file beign downloaded
        ** (diverse): All configuration available for Django's HttpResponse class
    """

    def __init__(self, request, path, filename, redirect_to=None, *args, **kwargs):
        super(DownloadResponse, self).__init__(*args, **kwargs)
        if not hasattr(path, '__call__') and not isinstance(path, str):
            raise ValueError(
                'DownloadResponse expects a callable object or str')

        # Convert to callable if it's a string
        self._get_path = path if hasattr(path, '__call__') else (lambda: path)
        self.path = self.get_path()
        self.filename = filename
        self.redirect_to = redirect_to or reverse_lazy('solicitacao:index')
        self.request = request

        self.get_response()

    def get_response(self):
        if self.path is None:
            self['Location'] = self.redirect_to
            self.status_code = 302
        elif re.match('/tmp/', self.path):  # force client to download attachment
            self.content = self.get_file_content()
            self['Content-Length'] = os.path.getsize(self.path)
            self['Content-Disposition'] = 'attachment; filename={}'.format(
                self.filename)
        elif re.match('https?://', self.path):  # redirect client
            self['Location'] = self.path
            self.status_code = 302

    def get_path(self):
        if not hasattr(self, '_path'):
            self._path = self._get_path()
        return self._path

    def get_file(self):
        if not hasattr(self, '_file'):
            self._file = open(self.path, 'rb')
            self._closable_objects.append(self._file)
        return self._file

    def get_file_content(self):
        return self.get_file().read()
