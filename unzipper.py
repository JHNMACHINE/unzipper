import os
import threading
import time

import patoolib
import send2trash
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class UnzipHandler(FileSystemEventHandler):
    def __init__(self):
        self.lock = threading.Lock()

    def process_existing_files(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if self.is_archive(file_path):
                    with self.lock:
                        try:
                            if self.is_download_complete(file_path):
                                self.extract_archive(file_path)
                        except FileNotFoundError:
                            # Gestisci il caso in cui il file non è ancora disponibile
                            pass

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = os.path.join(event.src_path)
        if self.is_archive(file_path):
            with self.lock:
                if self.is_download_complete(file_path):
                    self.extract_archive(file_path)

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = os.path.join(event.src_path)
        if self.is_archive(file_path):
            with self.lock:
                if self.is_download_complete(file_path):
                    self.extract_archive(file_path)

    def is_download_complete(self, file_path):
        # Verifica se il file è completo, ad esempio controllando se la dimensione è stabile da un po' di tempo.
        # Puoi personalizzare questa logica in base al tuo scenario specifico.
        try:
            time.sleep(0.5)  # Aspetta un po' prima di verificare la dimensione (personalizzabile)
            initial_size = os.path.getsize(file_path)
            time.sleep(0.5)  # Aspetta un altro po' prima di verificare di nuovo la dimensione
            final_size = os.path.getsize(file_path)

            return initial_size == final_size
        except FileNotFoundError:
            # Gestisci il caso in cui il file non è ancora disponibile
            return False

    def is_archive(self, file_path):
        _, extension = os.path.splitext(file_path)
        archive_extensions = {".zip", ".rar", ".7z", ".gz", ".bz2"}
        return extension.lower() in archive_extensions

    def extract_archive(self, archive_path):
        try:
            # Normalizza il percorso del file
            archive_path = os.path.normpath(archive_path)

            extract_folder = os.path.splitext(archive_path)[0]
            if not os.path.exists(extract_folder):
                print(f"Extracting archive: {archive_path}")
                patoolib.extract_archive(archive_path, outdir=extract_folder)
                print(f"Archive extracted successfully.")
            else:
                print(f"Destination folder already exists, skipping extraction: {extract_folder}")

            send2trash.send2trash(archive_path)
            print(f"Archive moved to trash: {archive_path}")

        except (patoolib.util.PatoolError, FileNotFoundError, OSError) as e:
            print(f"Error handling archive {archive_path}: {e}")


def watch_folder(folder_path):
    event_handler = UnzipHandler()
    # Processa i file esistenti
    event_handler.process_existing_files(folder_path)

    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)

    try:
        print(f"Watching folder: {folder_path}")
        observer.start()
        observer.join()
    except Exception as e:
        print(f"Error starting observer: {e}")
        observer.stop()


if __name__ == '__main__':
    folder_to_watch = os.path.expanduser("~/Downloads")
    watch_folder(folder_to_watch)
