import pandas as pd
import re
from glob import glob


def alternative_parents():
    try:
        file = open("all_classified.tsv", 'r')
        file_df = []
        df_1 = []
        for i, line in enumerate(file):
            if i >= 1000:
                break
            lines = line.strip().split("\t")
            file_df.append(lines)
        df_ap = pd.DataFrame(file_df)
        directory = glob("../processed_data/*/*.tsv")
        results = []
        for files in directory:
            if re.search(r"_rtdata_canonical_success.tsv", files):
                df_rt = pd.read_csv(files, sep='\t', header=0, encoding='utf-8')
                results.append(df_rt)
        if results:
            df_concat = pd.concat(results, axis=0, ignore_index=True)
            df_ap.rename(columns={0: "inchikey.std"}, inplace=True)
        for value in df_ap["inchikey.std"]:
            query = df_concat["inchikey.std"].str.contains(value, na=False)
            df_query = df_concat[query]
            if not df_query.empty:
                df_query.loc[0:, "inchikey.std"] = value
                df_1.append(df_query)
        df2 = pd.concat(df_1, axis=0, ignore_index=True)
        df = pd.merge(df2, df_ap, on="inchikey.std", how="inner")
        print(df)

    except Exception as e:
        print(f"Error: {e}")


alternative_parents()
