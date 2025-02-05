import os
import json

class Project:
    def __init__(self, cwd='./projects'):
        self.projectPath = cwd

    def read(self, filename):
        if os.path.exists(filename):
            f = open(filename, "r")
            data = f.read()
            try:
                return json.loads(data)
            except:
                return data
        return None

    def write(self, filename, data):
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            if isinstance(data, str):
                f = open(filename, "w")
                f.write(data)
                f.close()
            else:
                with open(filename, 'w') as file:
                    json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error writing to file {filename}: {e}")
            return False
    
    def update(self, filename, data: dict):
        try:
            existing_data = self.read(filename) or {}
            existing_data.update(data)
            success = self.write(filename, existing_data)
            return success
        except Exception as e:
            print(f"Error updating file {filename}: {e}")
            return False
    
    def remove_file(self, filename):
        filename = f"{filename}"
        if os.path.exists(filename):
            os.remove(filename)

    def openProject(self, projectPath=None):
        if projectPath:
            self.projectPath = projectPath
        self.project = self.read(f"{self.projectPath}/project.json")
        if not self.project:
            self.project = {}
        return self.project

    def saveProject(self):
        if self.project is None:
            self.project = {}
        self.update(f"{self.projectPath}/project.json", self.project)
        return
    
    