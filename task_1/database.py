import pandas as pd
import os
from datetime import datetime


class DatabaseManager:
    """
    A class to manage the CSV database for storing inputs and classifications.
    """

    def __init__(self, filepath: str = "database.csv"):
        self.filepath = filepath
        self.columns = ["Timestamp", "Input_Type", "Content", "Classification"]
        self._initialize_db()

    def _initialize_db(self):
        """Creates the CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.filepath):
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.filepath, index=False)
            print(f"Database initialized at {self.filepath}")

    def save_record(self, input_type: str, content: str, classification: str):
        """
        Saves a new record to the database.
        input_type: 'Text' or 'Image Caption'
        """
        try:
            new_data = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Input_Type": input_type,
                "Content": content,
                "Classification": classification
            }

            # Append to CSV without reading the whole file into memory
            df = pd.DataFrame([new_data])
            df.to_csv(self.filepath, mode='a', header=False, index=False)
            print("Record saved successfully.")

        except Exception as e:
            print(f"Error saving to database: {e}")

    def get_all_records(self) -> pd.DataFrame:
        """
        Retrieves all records from the database.
        """
        try:
            if os.path.exists(self.filepath):
                return pd.read_csv(self.filepath)
            return pd.DataFrame(columns=self.columns)
        except Exception as e:
            print(f"Error reading database: {e}")
            return pd.DataFrame(columns=self.columns)

    def clear_database(self):
        """Clears all records from the database."""
        try:
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.filepath, index=False)
        except Exception as e:
            print(f"Error clearing database: {e}")


# if __name__ == "__main__":
#     db = DatabaseManager()
#     print("Database is ready.")