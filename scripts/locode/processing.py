import os
import sys
sys.path.append(os.path.abspath(".."))

import csv
from datetime import datetime
from datetime import date
from pathlib import Path
from typing import List
from typing import Dict

import pandas as pd

from models.models import Actor, DataSource, ActorType

def write_csv(
    output_dir: str = None,
    name: str = None,
    data: List[Dict] | Dict = None,
    mode: str = "w",
    extension: str = "csv",
) -> None:
    """converts dictionary to CSV"""
    if isinstance(data, dict):
        data = [data]

    with open(f"{output_dir}/{name}.{extension}", mode=mode) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def main():

    # ------------------------------------------
    # datasource table
    # ------------------------------------------
    datasource_name = "locode"
    publisher = "unece"

    datasource = DataSource(
        id = f"{publisher}:{datasource_name}",
        name = "United Nations Code for Trade and Transport Locations",
        publisher = publisher,
        published_date = datetime.strptime( "2025-01-15", "%Y-%m-%d"),
        version = "v2024-2",
        url = "https://unece.org/trade/uncefact/unlocode",
    )

    # load data
    data_dir = Path(os.path.abspath(f"../data/{datasource_name}"))
    output_dir = data_dir / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    write_csv(
        output_dir=output_dir, name=datasource.__tablename__, data=datasource.model_dump(), mode="w"
    )

    # ------------------------------------------
    # actor table
    # ------------------------------------------

    # column names and descriptions here: https://service.unece.org/trade/locode/Service/LocodeColumn.htm
    columns = [
        "Ch",
        "Locode",
        "Name",
        "NameWoDiacritics",
        "SubDiv",
        "Function",
        "Status",
        "Date",
        "IATA",
        "Coordinates",
        "Remarks",
    ]

    files = [
        data_dir / "raw/loc242csv/2024-2 UNLOCODE CodeListPart1.csv",
        data_dir / "raw/loc242csv/2024-2 UNLOCODE CodeListPart2.csv",
        data_dir / "raw/loc242csv/2024-2 UNLOCODE CodeListPart3.csv",
    ]

    df_actors = pd.concat(
        [
            pd.read_csv("../data/iso-3166-1/processed/actor.csv"),
            pd.read_csv("../data/iso-3166-2/processed/actor.csv")
        ]
        )

    df = pd.concat([
        pd.read_csv(file, encoding="latin1", names=columns, keep_default_na=False)
        .reset_index(drop=True)
        #.query("Ch.isin(@df_actors['id'])") # must be in country in our database already
        .query("~Locode.eq('')")
        .loc[lambda x: x["Locode"].notnull()]
        #.query("Name.notnull()")
        #.query("SubDiv.notnull()")
        .assign(id = lambda x: x["Ch"] + x["Locode"])
        #.assign(is_part_of = lambda x: x["Ch"] + "-" + x["SubDiv"] if x["SubDiv"] else x["Ch"] )
        .assign(
            is_part_of = lambda x: x.apply(
            lambda row: row["Ch"] + "-" + row["SubDiv"] if row['SubDiv'] else row["Ch"],
            axis=1)
            )
        .query("is_part_of.isin(@df_actors['id'])") 
        .assign(datasource_id = datasource.id)
        .assign(type = "city")
        .rename(columns = {"NameWoDiacritics": "name"})
        [["id", "name", "is_part_of", "type", "datasource_id"]]
        .drop_duplicates()
        .drop_duplicates(subset="id", keep="first")
        #.to_csv(f"{output_dir}/actor.csv", index=False)
    
    for file in files
    ]
    )

    
    #df = (
    #    pd.read_csv(fl, keep_default_na=False)
    #    .assign(
    #        type = lambda x: x.apply(
    #        lambda row: "adm2" if row['parent_subdivision'] else "adm1",
    #        axis=1)
    #        )
    #    .assign(
    #        is_part_of = lambda x: x.apply(
    #        lambda row: row['parent_subdivision'] if row['parent_subdivision'] else row["#country_code_alpha2"],
    #        axis=1)
    #        )
    #    .rename(columns = {"subdivision_code_iso3166-2":"id", "subdivision_name": "name"})
    #    .assign(datasource_id = datasource.id)
    #    .sort_values(by = ["type", "id"])
    #    [["id", "name", "is_part_of", "type", "datasource_id"]]
    #    .drop_duplicates()
    #    .drop_duplicates(subset="id", keep="first")
    #)

    # === Manual topological sort ===
    # solves the dependency problem 
    # code from LLM, do not fully understand it. 
    
    #id_map = df.set_index("id")
    #visited = set()
    #ordered_ids = []

    #def visit(node):
    #    if node in visited or node not in id_map.index:
    #        return
    #    parent = id_map.at[node, "is_part_of"]
    #    if parent and parent in id_map.index:
    #        visit(parent)
    #   visited.add(node)
    #    ordered_ids.append(node)

    #for node in id_map.index:
    #    visit(node)

    # Apply the sorted order
    #df = id_map.loc[ordered_ids].reset_index()
    
    # === End Manual topological sort ===

    # data validation
    
    actors_validated = [
        Actor(
            id = row.id,
            name = row.name,
            is_part_of = row.is_part_of,
            type = ActorType(row.type),
            datasource_id = row.datasource_id
        ).model_dump()
        for row in df.itertuples()
    ]
    

    write_csv(
        output_dir=output_dir, name = Actor.__tablename__, data = actors_validated, mode="w"
    )
    
    return df



if __name__ == "__main__":
    df = main()
   # main()