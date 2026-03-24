import os
import uuid


class LocalFileStorage:
    def __init__(self, storage_dir: str = "storage"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_pdf(self, file_name: str, file_bytes: bytes) -> str:
        unique_name = f"{uuid.uuid4()}_{file_name}"
        file_path = os.path.join(self.storage_dir, unique_name)

        with open(file_path, "wb") as file:
            file.write(file_bytes)

        return file_path