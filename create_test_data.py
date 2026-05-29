import openpyxl
import os

os.makedirs("test_data", exist_ok=True)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Sheet1"

# Headers
ws.append(["username", "password", "expected_result", "test_type"])

# Data rows
ws.append(["student",   "Password123", "Logged In Successfully",    "valid"])
ws.append(["wronguser", "Password123", "Your username is invalid!", "invalid"])
ws.append(["student",   "wrongpass",   "Your password is invalid!", "invalid"])
ws.append(["",          "",            "Your username is invalid!", "empty"])

wb.save("test_data/login_data.xlsx")
print("✅ login_data.xlsx created successfully!")