import requests
from tqdm import tqdm


def download(url, dst, chunk_size=1024 * 4):
    """
    Downloads a file with a tqdm progress bar.
    """
    file_size = int(requests.head(url).headers["Content-Length"])
    req = requests.get(url, stream=True)
    with open(dst, 'xb') as f, tqdm(total=file_size, unit='B', unit_scale=True, desc=url.split('/')[-1]) as pbar:
        for chunk in req.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
            pbar.update(chunk_size)
        pbar.close()
