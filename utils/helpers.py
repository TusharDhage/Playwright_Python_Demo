import datetime

def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def take_screenshot(page, name="screenshot"):
    filename = f"reports/{name}_{get_timestamp()}.png"
    page.screenshot(path=filename)
    return filename