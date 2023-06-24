import requests

def get_summary_from_file(
    file_path: str, 
    summary_length: int = 50, 
    ip: str = '127.0.0.1', 
    port: int = 8000
    ):

    with open(file_path, 'r') as f:
        text = f.read()


    headers = {'Content-Type': 'application/json'}
    payload = {'text': text, 'summary_length': summary_length}

    r = requests.post(f"http://{ip}:{port}/summary", json=payload, headers=headers)

    return r

if __name__=='__main__':
    response = get_summary_from_file('article.txt')
    print(response.text)