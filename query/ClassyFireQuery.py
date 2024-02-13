import re
import pandas as pd
import sys
from glob import glob
import os
import numpy as np


def is_isomeric(smiles):
    return any(c in smiles for c in ['\\', '/', '@'])


def access_metadata(file):
    try:
        met = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
        return met
    except Exception as e:
        print(f"Error metadata:{e}")


def access_gradient(file):
    try:
        gra = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
        return gra
    except Exception as e:
        print(f"Error gradient data:{e}")


def access_descriptors(file):
    try:
        des = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
        return des
    except Exception as e:
        print(f"Error descriptors data:{e}")


def access_data(pattern, location=".*"):
    try:
        directory = glob("../processed_data/*/*.tsv")
        results = []
        info = []
        for file in directory:
            if re.search(r"_metadata.tsv", file):
                met = access_metadata(file)
            if re.search(r"_gradient.tsv", file):
                gra = access_gradient(file)
            if re.search(r"_descriptors_isomeric_", file):
                des = access_descriptors(file)
            df = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
            if "classyfire.kingdom" in df.columns and is_isomeric(df['smiles.std'].iloc[0]):
                column = df.filter(regex=f'{location}', axis=1)
                column_string = column.select_dtypes(include=['object'])
                for col in column_string.columns:
                    query = column[col].str.lower().str.contains(pattern.lower(), na=False)
                    if not df[query].empty and len(results) < 5:
                        df_concat = pd.merge(df[query], des, on=["id", "id"], how="left")
                        data = [gra, met, df_concat]
                        results.append(df_concat)
                        info.append(data)
                        break
        if column.size == 0:
            print(f"{location} not found")
        elif results:
            for i in info:
                print(f"\nColumn gradient:\n{i[0]} \nColumn data:\n{i[1]} \nMolecule data:\n {i[2]}")
            # concat = pd.concat(results, axis=0)
            # print(concat)
        else:
            print(f'No matches found with {pattern}')
    except Exception as e:
        print(f"Error:{e}")


access_data("lipids")
