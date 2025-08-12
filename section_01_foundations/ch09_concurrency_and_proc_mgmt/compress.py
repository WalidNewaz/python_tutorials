import gzip
import shutil
from multiprocessing import Pool
from pathlib import Path

def compress_file(file_path):
    compressed_path = f"{file_path}.gz"
    with open(file_path, 'rb') as f_in, gzip.open(compressed_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    return compressed_path

def get_files(directory):
    return [str(p) for p in Path(directory).glob('*.log')]

if __name__ == '__main__':
    files = get_files('data')
    with Pool() as pool:
        results = pool.map(compress_file, files)
    print(f"Compressed: {results}")