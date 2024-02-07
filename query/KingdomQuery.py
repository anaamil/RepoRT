import pandas as pd
import sys
from glob import glob
import os

def is_isomeric(smiles):
    return any(c in smiles for c in ['\\', '/', '@'])

def acceso_data_kingdom(kingdom):
    try:
        directory = glob("../processed_data/*/*_success.tsv")
        resultado=[]
        for file in directory:
            df = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
            if "classyfire.kingdom" in df.columns:
                query=df["classyfire.kingdom"].str.contains(kingdom, na=False)
                if not df[query].empty and len(resultado)<10 and is_isomeric(df['smiles.std'].iloc[0]):
                    resultado.append(df[query])
        if resultado:
            for i in resultado:
                print(i)
        else:
            print(f'No se han encontrado coincidencias con {kingdom}')
    except Exception as e:
        print(f"Error:{e}")

def acceso_data_superclass(superclass):
    try:
        directory = glob("../processed_data/*/*_success.tsv")
        resultado=[]
        for file in directory:
            df = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
            if "classyfire.superclass" in df.columns:
                columna=df["classyfire.superclass"].str.lower()
                query=columna.str.contains(superclass.lower(), na=False)
                if not df[query].empty and len(resultado)<10 and is_isomeric(df['smiles.std'].iloc[0]):
                    resultado.append(df[query])
        if resultado:
            for i in resultado:
                print(i)
        else:
            print(f'No se han encontrado coincidencias con {superclass}')
    except Exception as e:
        print(f"Error:{e}")

def acceso_metadata(file):
    try:
        if os.path.basename(file) == "*_metadata.tsv":
            ser = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
            col_crom = ser['column.name']
            return col_crom
    except Exception as e:
        print(f"Error:{e}")

def acceso_data(patron):
    try:
        directory = glob("../processed_data/*/*.tsv")
        resultado=[]
        for file in directory:
            col_crom=acceso_metadata(file)
            if col_crom is not None:
                col_name = col_crom
            df = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
            if "classyfire.kingdom" in df.columns and is_isomeric(df['smiles.std'].iloc[0]):
                columna = df.filter(regex='classyfire.*')
                for col in columna.columns:
                    query = columna[col].str.lower().str.contains(patron.lower(), na=False)
                    if not df[query].empty and len(resultado)<5:
                        #print(col_name)
                        resultado.append(df[query])
                        break
        if resultado:
            for i in resultado:
                print(i)
        else:
            print(f'No se han encontrado coincidencias con {patron}')
    except Exception as e:
        print(f"Error:{e}")

#acceso_data_kingdom("Organic")
#acceso_data_superclass("Nucleosides")
acceso_data("Nucleosides")

