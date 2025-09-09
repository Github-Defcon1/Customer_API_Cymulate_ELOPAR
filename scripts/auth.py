class authenticate():
    def __init__(self):
        pass

    def create_headers(self, xtoken):
        headers = {
            "x-token": f"{xtoken}"
        }
        return headers