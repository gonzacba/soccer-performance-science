import pandas as pd
import os

folders = ['wellness', 'training-load', 'injury', 'illness', 'game-performance']

for folder in folders:
    path = f'data/raw/{folder}'
    files = os.listdir(path)
    print(f'\n--- {folder} ---')
    print(f'Files: {len(files)} | First file: {files[0]}')
    first_file = f'{path}/{files[0]}'
    if files[0].endswith('.csv'):
        df = pd.read_csv(first_file)
        print(f'Shape: {df.shape}')
        print(f'Columns: {list(df.columns)}')
        print(df.head(2))