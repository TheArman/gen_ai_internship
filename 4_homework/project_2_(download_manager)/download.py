"""Download modul"""

from abc import ABC, abstractmethod
import threading
import multiprocessing
import requests


def download_file(url):
    """
        This function takes parameter
        Arg:
            url: str,
        send request for url, and downloads the context,
        if it http/https or ftp file.
    """

    if url.startswith('http') or url.startswith('ftp'):
        try:
            target = requests.get(url)
            return target.content
        except Exception(f'Invalid url {url}') as e:
            return e


class Download(ABC):
    """
        This is abstract class with start_download abstract method.
        Takes two mandatory arguments
        Args:
            url: str and filename: str.
        This class helps download HTTP/HTTPS/FTP files.
    """

    def __init__(self, url, filename):
        self._url = url
        self._filename = filename
        self._complete = False

    @property
    def url(self):
        return self._url

    @property
    def filename(self):
        return self._filename

    @abstractmethod
    def start_download(self):
        ...

    def save_file(self, content):
        """
            This method takes parameter content:
            bytes and writing it into file.
        """

        with open(self._filename, 'wb') as file:
            print(f'Writing content of {self.url} into {self._filename}')
            file.write(content)

    def download_complete(self):
        """
            This method helps us to know that downloading
            successfully finished.
        """
        print(f'Download completed ({self.url})')
        self._complete = True


class ThreadingDownloader(Download):
    """
        This class extends Download Class and implements start_download method,
        where use threads.
    """

    def start_download(self):
        """
            Use this function for start downloading, using threading.
        """
        downloaded_file = download_file(self.url)
        thread = threading.Thread(target=self.save_file, args=(downloaded_file,))
        print(f'Download started {self.url} with {thread.getName}')
        thread.start()
        # thread.join()
        self.download_complete()


class MultiprocessingDownloader(Download):
    """
    This class extends Download Class and implements start_download method,
    where use multiprocessing.
    """

    def start_download(self):
        """
            Use this function for start downloading, using multiprocessing.
        """

        downloaded_file = download_file(self.url)
        process = multiprocessing.Process(target=self.save_file, args=(downloaded_file,))
        process.start()
        print(f'Process ID: {process.pid}')
        self.download_complete()
