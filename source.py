"""
Source module for CSV Anonymizer.
Defines the Source class for representing data sources.
"""


class Source:
    """
    Represents a data source (file or database).
    
    Attributes:
        name: Name of the source (filename or connection string)
        sub_source: Sub-source identifier (e.g., table name for databases)
    """
    
    def __init__(self, name: str, sub_source: str = None):
        self.name = name
        self.sub_source = sub_source
    
    def __hash__(self) -> int:
        return hash((self.name, self.sub_source))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Source):
            return False
        return (self.name, self.sub_source) == (other.name, other.sub_source)

    def __str__(self) -> str:
        return f"Source: {self.name}, Sub Source: {self.sub_source}"
