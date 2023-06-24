import argparse
import requests

def get_summary_from_file(
    file_path: str, 
    summary_length: int,
    ip: str, 
    port: int 
):
    '''
    Function to POST data for summary to the FastAPI summarization service.

    Args:
        file_path (str): Path mapping to file with text to summarize.
        summary_length (int): Maximum allowable word length of summary.
        ip (str): IP of the summarization service.
        port (int): Port of the summarization service.
    '''
    with open(file_path, 'r') as f:
        text = f.read()


    headers = {'Content-Type': 'application/json'}
    payload = {'text': text, 'summary_length': summary_length}

    r = requests.post(f'http://{ip}:{port}/summary', json=payload, headers=headers)

    return r

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default='article.txt', help='Path to text file to summarize')
    parser.add_argument('-l', '--length', default=50, help='Requested summary length')
    parser.add_argument('-i', '--ip', default='127.0.0.1', help='Host name of summarization service')
    parser.add_argument('-p', '--port', default=8000, help='Port of summarization service')

    args = parser.parse_args()

    response = get_summary_from_file(
        file_path=args.file, summary_length=args.length, ip=args.ip, port=args.port
    )

    print(response.text)

