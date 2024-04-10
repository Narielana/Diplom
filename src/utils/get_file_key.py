def get_file_by_path(path: str):
    try:
        with open(path, 'r') as f:
            key = f.read()
        return key
    except:
        return '123'
