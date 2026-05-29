import csv
import os
import pandas as pd


class DataReader:

    @staticmethod
    def read_csv(file_name: str) -> list[dict]:
        """Read test data from CSV file"""
        file_path = os.path.join(
            os.path.dirname(__file__),
            "..", "test_data", file_name
        )
        data = []
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(dict(row))
        return data

    @staticmethod
    def read_excel(file_name: str, sheet_name: str = "Sheet1") -> list[dict]:
        """Read test data from Excel file"""
        file_path = os.path.join(
            os.path.dirname(__file__),
            "..", "test_data", file_name
        )
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df = df.fillna("")   # replace NaN with empty string
        return df.to_dict(orient="records")

    @staticmethod
    def get_valid_credentials_csv() -> list[dict]:
        """Return only valid login rows from CSV"""
        data = DataReader.read_csv("login_data.csv")
        return [row for row in data if row["test_type"] == "valid"]

    @staticmethod
    def get_invalid_credentials_csv() -> list[dict]:
        """Return only invalid login rows from CSV"""
        data = DataReader.read_csv("login_data.csv")
        return [row for row in data if row["test_type"] == "invalid"]

    @staticmethod
    def get_all_credentials_excel() -> list[dict]:
        """Return all login rows from Excel"""
        return DataReader.read_excel("login_data.xlsx")