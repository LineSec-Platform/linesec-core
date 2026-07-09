from pydantic import BaseModel

class FindingCreate(BaseModel):
    tool_name: str
    vulnerability_name: str
    severity: str
    description: str
    file_path: str
    line_number: int
