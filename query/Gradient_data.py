import re
import pandas as pd
import sys
from glob import glob
import os
import numpy as np
import matplotlib.pyplot as plt


def gradient_data():
    try:
        directory = glob("../processed_data/*/*.tsv")
        gradient = []
        time_dic = []
        dictionary = {}
        column_data, eluent_data, gra_data = metadata()
        for file in directory:
            if re.search(r"_gradient.tsv", file):
                gra = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
                file_name = os.path.basename(file)
                if gra["t [min]"].isnull().values.any() or gra["t [min]"].values.size == 0:
                    gradient.append(file_name)
                else:
                    dictionary[file_name[0:4]] = gra["t [min]"].values.max(), gra.values.shape[0]
                    lista = []
                    gra["file"] = int(file_name[0:4])
                    gra_i = gra.set_index("file")
                    for i in range(gra_i.shape[0]):
                        gra_d = gra_i.rename(columns={'t [min]': f't {i}', 'A [%]': f'A {i}', 'B [%]': f'B {i}', 'C [%]': f'C {i}', 'D [%]': f'D {i}', 'flow rate [ml/min]': f'flow rate {i}'})
                        g = gra_d.iloc[i, 0:7]
                        elu = eluent_data.rename(columns={col: f'{col} {i}' for col in eluent_data.columns})
                        lista.append(pd.concat([elu.loc[int(file_name[0:4])], g]))
                    df_g = pd.DataFrame(pd.concat(lista)).transpose()
                    df_merge = pd.merge(column_data, df_g, left_index=True, right_index=True, how="right")
                    time_dic.append(df_merge)
        df = pd.concat(time_dic, axis=0)

        # df.to_csv("..\..\data.tsv", sep="\t", index=True)
        # df_t = pd.DataFrame(data=dictionary, index=["t_max","num"])
        # df_transpose = df_t.transpose()
        # t_max = df_transpose["t_max"].max()
        # num = df_transpose["num"].max()
        # df_transpose.to_csv("..\..\gradient.tsv", sep="\t", index=True)
        # print(t_max, num)
        # plt.hist(df_transpose["t_max"], bins=int(t_max+1), alpha=0.5, color='blue', edgecolor='black')
        # plt.show()
        # plt.hist(df_transpose["num"], bins=int(num+1), color="green", edgecolor='black')
        # plt.show()
        print(len(gradient))
    except Exception as e:
        print(e)


def metadata():
    try:
        directory = glob("../processed_data/*/*.tsv")
        metadata = []
        for file in directory:
            if re.search(r"_metadata.tsv", file):
                met = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
                metadata.append(met)
        df_met = pd.concat(metadata, ignore_index=True)
        #columns_to_drop = [col for col in df_met.columns if '.C' in col or '.D' in col]
        df_filtered = df_met.set_index("id")
                       #.drop(columns=columns_to_drop).set_index("id")
        position = [pos for pos, col in enumerate(df_filtered.columns) if "unit" in col]
        for pos in position:
            if df_filtered.iloc[:, pos].notna().any() and df_filtered.iloc[:, pos].str.contains("mM").any():
                if "nh4ac" in df_filtered.columns[pos - 1]:
                    df_filtered.iloc[:, pos - 1] *= 0.007
                elif "nh4form" in df_filtered.columns[pos - 1]:
                    df_filtered.iloc[:, pos - 1] *= 0.005
                elif "nh4carb" in df_filtered.columns[pos - 1]:
                    df_filtered.iloc[:, pos - 1] *= 0.006
                elif "nh4bicarb" in df_filtered.columns[pos - 1]:
                    df_filtered.iloc[:, pos - 1] *= 0.005
                elif "nh4form" in df_filtered.columns[pos - 1]:
                    df_filtered.iloc[:, pos - 1] *= 0.004
                elif "nh4oh" in df_filtered.columns[pos - 1]:
                    df_filtered.iloc[:, pos - 1] *= 0.004
            elif df_filtered.iloc[:, pos].notna().any() and df_filtered.iloc[:, pos].str.contains("µM").any():
                if "phosphor" in df_filtered.columns[pos - 1]:
                    df_filtered.iloc[:, pos - 1] *= 5.21/(10**6)
                elif "medronic" in df_filtered.columns[pos - 1]:
                    df_filtered.iloc[:, pos - 1] *= 8.38/(10**6)
        for column in df_filtered.columns[2:9]:
            lines_null = df_filtered[df_filtered[column].isnull()]
            same_lines = df_filtered[df_filtered['column.name'].isin(lines_null["column.name"])]
            mean = same_lines.groupby('column.name')[column].mean()
            for index, mean in mean.items():
                df_filtered.loc[(df_filtered[column].isnull()) & (df_filtered['column.name'] == index), column] = mean
        #df = pd.merge(df_filtered, df_gra, left_index=True, right_index=True, how="left")
        column_data = df_filtered.iloc[:, 0:9]
        eluent_data = df_filtered.iloc[:, 9:168]
        gra_data = df_filtered.iloc[:, 168:]
        #df_met.to_csv("..\..\metadata.tsv", sep="\t", index=True)
        #df_filtered.to_csv("..\..\metadata_filtered.tsv", sep="\t", index=True)
        return column_data, eluent_data, gra_data
    except Exception as e:
        print(f"Error metadata:{e}")



gradient_data()

