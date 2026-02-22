########################################################################################
import os
import json
from icecream import ic    # pyright: ignore[reportMissingImports]
########################################################################################
class JsonDatabase:
    # constructor to create the database folder
    def __init__(self, base_path: str = ".db"):
        self.base_path: str = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    # helper to generate folder and file paths return tuple as (folder_path, file_path)
    def __get_paths(self, entity_name: str, record_id: str = None) -> tuple[str, str]:
        # create the folder path
        folder_path = os.path.join(self.base_path, entity_name)
        # create the folder in (os file system) if not exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # create the file path if record_id is provided
        file_path = os.path.join(folder_path, f"{record_id}.json")
        file_path = file_path if record_id else None
        # return the folder path and file path
        return folder_path, file_path

    # Saves a record using the centralized path helper
    def save_record(self, entity_name: str, record_id: str, data: object) -> None:
        # get the file path
        _, file_path = self.__get_paths(entity_name, record_id)
        # convert the data to a dictionary
        data = data.__dict__ if hasattr(data, "__dict__") else dict(data)
        # write the data to the file
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        # print a success message
        ic(f"Data Saved to: {file_path}")

    def get_record(self, entity_name: str, record_id: str) -> object | None:
        # get the file path
        _, file_path = self.__get_paths(entity_name, record_id)
        # check if the file exists
        if not os.path.exists(file_path):
            ic("File Not Found:", file_path)
            return None
        # load the data from the file
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        # print a success message
        ic(f"Data Loaded from: {file_path}")
        return data

    def delete_record(self, entity_name: str, record_id: str) -> bool:
        # get the folder and file path
        folder_path, file_path = self.__get_paths(entity_name, record_id)
        # check if the file exists then delete it
        if os.path.exists(file_path):
            os.remove(file_path)
            ic(f"Data Deleted from: {file_path}")
            # check if the folder is empty then remove it
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
                ic(f"Folder is Empty and Deleted: {folder_path}")
            return True
        # print a failure message if the file does not exist
        ic(f"File Not Found: {file_path}")
        return False

    # get all records in an entity folder in the database folder
    def get_all_records(self, entity_name: str) -> list[object] | None:
        # get the folder path
        folder_path = os.path.join(self.base_path, entity_name)
        # check if the folder exists
        if not os.path.exists(folder_path):
            ic(f"Folder Not Found: {folder_path}")
            return None
        # get the file paths
        record_ids = [
            filename[:-5] for filename in os.listdir(folder_path)
            if filename.endswith('.json')
        ]
        # load the data from the files
        data = [
            self.get_record(entity_name, record_id)
            for record_id in record_ids
        ]
        # print a success message
        ic(f"All Records Loaded From: {folder_path}")
        return data

    def get_record_count(self, entity_name: str) -> int:
        # get the folder path
        folder_path = os.path.join(self.base_path, entity_name)
        # check if the folder exists
        if not os.path.exists(folder_path):
            ic(f"Folder Not Found: {folder_path}")
            return 0
        # get a list of all json files names
        files = [
            filename for filename in os.listdir(folder_path)
            if filename.endswith('.json')
        ]
        # return the number of records
        ic(f"Found ({len(files)}) Records in Folder: {folder_path}")
        return len(files)

    @property
    def entities_list(self) -> list[str]:
        # get a list of all entity names
        return [
            entity_name for entity_name in os.listdir(self.base_path)
            if os.path.isdir(os.path.join(self.base_path, entity_name))
        ]

    @property
    def entities_dict(self) -> dict[str, int]:
        # get a dictionary of each entity name and their records count
        return {
            entity_name: self.get_record_count(entity_name)
            for entity_name in self.entities_list
        }

    def __str__(self):
        return (
            f"JsonDatabase(base_path={self.base_path}, "
            f"entities={self.entities_list})"
        )

    def __repr__(self):
        return (
            f"JsonDatabase(base_path={self.base_path}, "
            f"entities={self.entities_dict})"
        )
