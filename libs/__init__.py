import os


def get_data_dir() -> str:
    data_dir = os.getenv("DATA_DIR", "/data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir

