######################################################################################
from uuid import uuid4
######################################################################################
class Department:
    def __init__(self, name: str, description: str):
        self.id = str(uuid4())
        self.name = name
        self.description = description

    def __str__(self):
        return f"""-------------------
    id: {self.id}
    name: {self.name}
    description: {self.description}
    ---------------------"""
    def __repr__(self):
        return f"Department(id={self.id}, name={self.name}, description={self.description})"
