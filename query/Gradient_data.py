import re
import pandas as pd
import sys
from glob import glob
import os
import numpy as np


def gradient_data():
    try:
        directory = glob("../processed_data/*/*.tsv")
        gradient = []
        dictionary = {}
        for file in directory:
            if re.search(r"_gradient.tsv", file):
                try:
                    gra = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
                except Exception as e:
                    print(f"Error gradient:{e}")
                file_name = os.path.basename(file)
                if gra["t [min]"].isnull().values.any() or gra["t [min]"].values.size == 0:
                    gradient.append(file_name)
                else:
                    dictionary[file_name] = gra["t [min]"].values.max(), gra.values.shape[0], gra["t [min]"].diff().mean()

        df = pd.DataFrame(data=dictionary, index=["t_max","num","mean"])
        df_transpose = df.transpose()
        t_max = df_transpose["t_max"].max()
        num = df_transpose["num"].max()
        mean = df_transpose["mean"].max()

        print(t_max, num, mean)

    except Exception as e:
        print(e)


gradient_data()