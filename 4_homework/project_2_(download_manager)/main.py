import manager

download_manager = manager.DownloadManager(max_threads=3, max_processes=2)

download_manager.download("http://example.com/file1.txt", "file1.txt")
# download_manager.download("ftp://example.com/file2.txt", "file2.txt")
download_manager.download("http://example.com/file3.txt", "file3.txt")

download_manager.start()
download_manager.wait()

print("All downloads completed!")
