"""Manager modul"""

from download import ThreadingDownloader, MultiprocessingDownloader
import threading
import multiprocessing


class DownloadManager:
    """
        This class manages downloaders, takes two arguments
        Args:
            max_threads: int, min_threads: int.
    """

    def __init__(self, max_threads, max_processes):
        self._max_threads = max_threads
        self._max_processes = max_processes
        self._downloads = []

    @property
    def max_threads(self):
        return self._max_threads

    @property
    def max_processes(self):
        return self._max_processes

    @property
    def downloads(self):
        return self._downloads

    def download(self, url, filename):
        """
            This method downloads and added it into downloaders list.
        """

        download_file = MultiprocessingDownloader(url, filename)
        self.downloads.append(download_file)

    def start(self):
        """
            This method starts downloading and checks counts
                 of threads and processes.
        """

        for file in self.downloads:
            if len(multiprocessing.active_children()) < self.max_processes:
                MultiprocessingDownloader.start_download(file)

            elif threading.active_count() < self.max_threads:
                ThreadingDownloader.start_download(file)


    def wait(self):

        """
            This method waits while all downloads finish successfully.
        """

        if len(self.downloads) > 0:
            for file in self.downloads:
                while not file._complete:
                    pass
            print('Installed Successfully')
