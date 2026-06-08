import flet as ft

import datetime
from pathlib import Path
import shutil
import zipfile
import tempfile

import json

import gc
import sqlite3


from AppState import AppState


class BackupManager():
    def __init__(self, app_state: AppState):
        self.page       = app_state.page

        self.app_state  = app_state

        self.database   = self.app_state.database
        self.settings   = self.app_state.settings
        self.translator = self.app_state.translator
        self.colors     = self.app_state.colors
        
        self.backup_registry_path = self.app_state.app_dir / "backups_registry.json"
        
    
    def get_backup_file_paths(self, extension: str = "db") ->  list[dict]:
        """
            Returns a list of backups of the passed extension.\n
            Order by: st_mtime DESC
        """
        is_desktop = self.app_state.platform in ("windows", "macos", "linux")

        backups    = []
        deleted_backups = []

        for backup in self.backup_registry:
            path = backup.get("path", "Does not exist")

            if is_desktop and ((path == "Does not exist") or (not Path(path).exists())):
                deleted_backups.append(backup)
                continue

            if backup.get("type", "").lower() == extension.replace(".", "").lower():
                backups.append(backup)

        if deleted_backups:
            self._backup_registry = [b for b in self.backup_registry if b not in deleted_backups]

            with open(self.backup_registry_path, "w", encoding="UTF-8") as file:
                json.dump(self._backup_registry, file, ensure_ascii=False, indent=4)


        return sorted(backups, key=lambda backup: backup.get("ctime", 0), reverse=True)



    async def export_database(self, file_picker: ft.FilePicker, dialog_title: str | None = None):
        export_time = datetime.datetime.now()
        file_name   = f"CycleDatabase_backup_from_{export_time.strftime('%d_%m_%Y_%H_%M_%S')}.db"
        db_bytes    = self.database._prepare_for_export_()

        
        self.saved_file_path = await file_picker.save_file(
            dialog_title=       dialog_title,
            file_name=          file_name,
            initial_directory=  self.settings.db_backups_dir if self.settings.db_backups_dir != "" else str(self.app_state.app_dir),
            allowed_extensions= ["db"],
            src_bytes=          db_bytes
        )

        if not self.saved_file_path:
            return None
        
       
        self.saved_file_path    = Path(self.saved_file_path)
        file_name               = self.saved_file_path.name
        self.destination_dir    = self.saved_file_path.parent

        is_desktop = self.app_state.platform in ("windows", "macos", "linux") if self.app_state.platform is not None else False

        # Перемещение файла резервной копии в специальную папку
        # выполняется только на платформах где это возможно ("windows", "macos", "linux")
        if is_desktop: 
            if self.destination_dir.name.lower() != self.app_state.backups_dir_name.lower():
                self.destination_dir = self.destination_dir / self.app_state.backups_dir_name

            self.destination_dir.mkdir(parents=True, exist_ok=True)

            if not self.destination_dir.is_dir():
                raise NotADirectoryError(f"Expected a folder, but found a file along the way: {self.destination_dir}")

            self.destination_file_path = self.destination_dir / file_name
            shutil.move(str(self.saved_file_path), str(self.destination_file_path))

        final_path = str(self.destination_dir / file_name) if is_desktop else str(self.saved_file_path)
        self.add_backup_record(
            {
                "name"  : file_name,
                "path"  : final_path,
                "ctime" : int(export_time.timestamp()),
                "size"  : len(db_bytes) if db_bytes is not None else 0,
                "type"  : "db"
            }
        )

        # Далее стандартное поведение для всех ОС
        self.settings.change_db_backups_dir(self.destination_dir)
        self.page.run_task(self.app_state.hot_restart_app)

        return True



    async def import_database(self, file_picker: ft.FilePicker, dialog_title: str | None = None):
        self.imported_file_path = await file_picker.pick_files(
            dialog_title=       dialog_title,
            initial_directory=  self.settings.db_backups_dir if self.settings.db_backups_dir != "" else str(self.app_state.app_dir),
            allowed_extensions= ["db", "sqlite"],
            allow_multiple=     False
        )
        
        if (not self.imported_file_path) or (self.imported_file_path[0].path is None):
            return None
        
        self.imported_file_path = Path(self.imported_file_path[0].path)

        self._validate_sqlite_file_(self.imported_file_path)
        self.database._prepare_for_import_()
        
        gc.collect()

        shutil.copy2(self.imported_file_path, self.database.db_path)

        # Добавление импортированного файла в реестр
        self.add_backup_record({
            "name"  : self.imported_file_path.name,
            "path"  : str(self.imported_file_path),
            "ctime" : int(self.imported_file_path.stat().st_mtime),
            "size"  : self.imported_file_path.stat().st_size,
            "type"  : "db"
        })

        self.page.run_task(self.app_state.hot_restart_app)

        return True




    async def export_archive(self, file_picker: ft.FilePicker, dialog_title: str | None = None, extension: str = "zip"):
        export_time     = datetime.datetime.now()
        file_name       = f"Cycle_backup_from_{export_time.strftime('%d_%m_%Y_%H_%M_%S')}.{extension.replace(".", "")}"
        archive_bytes   = self.create_zip_backup_bytes()

        
        self.saved_file_path = await file_picker.save_file(
            dialog_title=       dialog_title,
            file_name=          file_name,
            initial_directory=  self.settings.archive_backups_dir if self.settings.archive_backups_dir != "" else str(self.app_state.app_dir),
            allowed_extensions= [extension.replace(".", "")],
            src_bytes=          archive_bytes
        )

        if not self.saved_file_path:
            return None
        

        self.saved_file_path        = Path(self.saved_file_path)
        file_name                   = self.saved_file_path.name
        self.destination_dir        = self.saved_file_path.parent


        is_desktop = self.app_state.platform in ("windows", "macos", "linux") if self.app_state.platform is not None else False

        # Перемещение файла резервной копии в специальную папку
        # выполняется только на платформах где это возможно ("windows", "macos", "linux")
        if is_desktop: 
            if self.destination_dir.name.lower() != self.app_state.backups_dir_name.lower():
                self.destination_dir = self.destination_dir / self.app_state.backups_dir_name

            self.destination_dir.mkdir(parents=True, exist_ok=True)

            if not self.destination_dir.is_dir():
                raise NotADirectoryError(f"Expected a folder, but found a file along the way: {self.destination_dir}")

            self.destination_file_path = self.destination_dir / file_name
            shutil.move(str(self.saved_file_path), str(self.destination_file_path))


        final_path = str(self.destination_dir / file_name) if is_desktop else str(self.saved_file_path)
        self.add_backup_record(
            {
                "name"  : file_name,
                "path"  : final_path,
                "ctime" : int(export_time.timestamp()),
                "size"  : len(archive_bytes) if archive_bytes is not None else 0,
                "type"  : extension.replace(".", "")
            }
        )

        # Далее стандартное поведение для всех ОС
        self.settings.change_archive_backups_dir(self.destination_dir)
        self.page.run_task(self.app_state.hot_restart_app)

        return True



    async def import_archive(self, file_picker: ft.FilePicker, dialog_title: str | None = None, extension: str = "zip"): 
        self.imported_file_path = await file_picker.pick_files(
            dialog_title=       dialog_title,
            initial_directory=  self.settings.archive_backups_dir if self.settings.archive_backups_dir != "" else str(self.app_state.app_dir),
            allowed_extensions= [extension.replace(".", "")],
            allow_multiple=     False
        )
        
        if (not self.imported_file_path) or (self.imported_file_path[0].path is None):
            return None
        
        self.imported_file_path = self.imported_file_path[0].path

        # Извлечение данных во временную папку
        temp_dir = Path(tempfile.mkdtemp())
        with zipfile.ZipFile(self.imported_file_path, 'r') as zipf:
            zipf.extractall(temp_dir)
        
        # Проверка БД на целостность
        temp_db = temp_dir / "CycleDatabase.db"
        if not temp_db.exists():
            raise ValueError("The selected archive backup does not contain a database file")

        self._validate_sqlite_file_(temp_db)
            

        # Жесткая проверка на соответствие версии приложения
        temp_settings = temp_dir / "settings.json"
        if not temp_settings.exists():
            raise ValueError("The selected archive backup does not contain a settings file")

        with open(temp_settings, "r") as file:
            _settings_dict = dict(json.load(file))

        for version_part_index in range(len(_settings_dict["app_version"].split("."))):
            imported_version_part   = _settings_dict["app_version"].split(".")[version_part_index]
            current_version_part    = self.settings.app_version.split(".")[version_part_index]

            if imported_version_part > current_version_part:
                raise ValueError("Importing a backup copy of a newer version of the application is not allowed")
            


        # МЕСТО ДЛЯ ДОПОЛНИТЕЛЬНЫХ ПРОВЕРОК ФАЙЛОВ ИЗ АРХИВА РЕЗЕРВНОЙ КОПИИ
        # ВОЗМОЖНО ДОБАВЛЕНИЕ ПРОВЕРОК НА СООТВЕТСТВИЕ ВЕРСИИ И ИХ МИГРАЦИИ
        self.database._prepare_for_import_()
        
        # Замена всех файлов приложения на файлы из резервной копии
        if self.app_state.app_dir.exists():
            shutil.copytree(temp_dir, self.app_state.app_dir, dirs_exist_ok=True)


        # Добавление импортированного файла в реестр
        imported_path = Path(self.imported_file_path)
        self.add_backup_record({
            "name"  : imported_path.name,
            "path"  : str(imported_path),
            "ctime" : int(imported_path.stat().st_mtime),
            "size"  : imported_path.stat().st_size,
            "type"  : extension.replace(".", "")
        })


        self.page.run_task(self.app_state.hot_restart_app)

        return True





    def create_zip_backup_bytes(self) -> bytes:
        """
        Creates ZIP archive of all data of the app and returns a bit representation
        """

        zip_path = Path(self.app_state.app_dir) / "temp_zip_backup.zip"

        # Создание временного ZIP архива для создания бэкапа
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Добавление базы данных в архив
            if self.app_state.db_path.exists():
                zipf.write(self.app_state.db_path, "CycleDatabase.db")

            # Добавление файла настроек в архив
            if self.app_state.settings_path.exists():
                zipf.write(self.app_state.settings_path, "settings.json")

            # Добавление папки языковых пакетов в архив
            language_packs_dir_path = self.app_state.app_dir / "language_packs"
            if language_packs_dir_path.exists():
                for file_path in language_packs_dir_path.rglob("*"):
                    if file_path.is_file():
                        archive_name = file_path.relative_to(self.app_state.app_dir)
                        zipf.write(file_path, archive_name)


        with open(zip_path, "rb") as f:
            zip_bytes = f.read()

        zip_path.unlink()
    
        return zip_bytes



    
    def _validate_sqlite_file_(self, path: str | Path):
        try:
            with sqlite3.connect(path, check_same_thread=False, timeout=10) as conn:
                cur = conn.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1;")
                cur.execute("PRAGMA integrity_check")

        except sqlite3.DatabaseError:
            raise ValueError("The selected file is corrupted or is not a SQLite database.")
        



    @property
    def backup_registry_path(self) -> str:
        return str(self._backup_registry_path)
    
    
    @backup_registry_path.setter
    def backup_registry_path(self, registry_path: str | Path) -> None:
        self._backup_registry_path  = Path(registry_path)
        self._backup_registry       = None

        if not self._backup_registry_path.exists():
            with open(self.backup_registry_path, "w", encoding="UTF-8") as file:
                json.dump([], file)

        _ = self.backup_registry


    @property
    def backup_registry(self) -> list:
        try:
            if self._backup_registry is None:
                with open(self.backup_registry_path, "r", encoding="UTF-8") as file:
                    self._backup_registry = list(json.load(file))

        except (json.JSONDecodeError, IOError):
            self._backup_registry = []

        return self._backup_registry

        

    def add_backup_record(self, backup: dict[str, str | int | float]) -> None:
        self._backup_registry = None

        # Словарь автоматически перезапишет дубликат по ключу "name"
        registry_dict = {item["name"]: item for item in self.backup_registry}
        registry_dict[backup["name"]] = backup
        
        self._backup_registry = list(registry_dict.values())
        
        with open(self.backup_registry_path, "w", encoding="UTF-8") as file:
            json.dump(self._backup_registry, file, ensure_ascii=False, indent=4)
