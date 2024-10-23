import os

class StorageService:
    def __init__(self):
        self.upload_folder = os.path.join(os.getcwd(), 'static', 'uploads')
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
    
    def save_file(self, file, filename):
        file_path = os.path.join(self.upload_folder, filename)
        file.save(file_path)
        return f'/static/uploads/{filename}'
