import pandas as pd

if __name__ == '__main__':
    data1 = pd.read_csv(".\\databases\\cluster.data")
    print(data1.head())
    