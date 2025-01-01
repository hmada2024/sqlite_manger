import pandas as pd
from typing import List, Dict, Any

class FileOperations:
    @staticmethod
    def export_to_excel(data: List[Dict[str, Any]], filename: str):
        """Export data to Excel file"""
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
    
    @staticmethod
    def import_from_excel(filename: str) -> List[Dict[str, Any]]:
        """Import data from Excel file"""
        df = pd.read_excel(filename)
        return df.to_dict('records')