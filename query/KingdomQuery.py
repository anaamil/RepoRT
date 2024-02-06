import pandas as pd
import sys
from glob import glob
import re
def is_isomeric(smiles):
    return any(c in smiles for c in ['\\', '/', '@'])

def acceso_data(kingdom):
    try:
        directory = glob("../processed_data/*/*_success.tsv")
        resultado=[]
        for file in directory:
            df = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
            if "classyfire.kingdom" in df.columns:
                condition=df["classyfire.kingdom"]==kingdom
                if not df[condition].empty and len(resultado)<10:
                    resultado.append(df[condition])
        if resultado:
            for i in resultado:
                print(i)
    except Exception as e:
        print(f"Error:{e}")



acceso_data("C44H84NO8P")