# pip install gdown
import re
import requests


def extract_file_id(url_or_id: str) -> str:
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url_or_id)
    if match:
        return match.group(1)
    match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', url_or_id)
    if match:
        return match.group(1)
    return url_or_id


def install(url_or_id: str, destination_path: str = 'downloaded_file.zip', on_progress=None) -> str:
    file_id = extract_file_id(url_or_id)
    session = requests.Session()

    url = 'https://drive.google.com/uc'
    params = {'id': file_id, 'export': 'download'}

    response = session.get(url, params=params, stream=True)

    # Если сразу отдаётся файл - Content-Disposition будет в заголовках
    if 'content-disposition' not in response.headers:
        # значит это HTML-страница подтверждения - парсим форму
        html = response.text

        action_match = re.search(r'action="([^"]+)"', html)
        if not action_match:
            raise RuntimeError('Не удалось найти форму подтверждения скачивания. Проверьте ссылку/доступ.')

        action_url = action_match.group(1).replace('&amp;', '&')

        inputs = dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', html))

        response = session.get(action_url, params=inputs, stream=True)

    if 'content-disposition' not in response.headers:
        raise RuntimeError('Не удалось получить файл напрямую. Возможно, файл не публичный или превышена квота Google Drive на скачивание.')

    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0

    with open(destination_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    percent = int(downloaded * 100 / total_size)
                else:
                    percent = downloaded
                if on_progress:
                    on_progress(percent)

    return destination_path

if __name__ == "__main__":
    install(
        'url',
        on_progress=lambda mb: print(mb)
    )