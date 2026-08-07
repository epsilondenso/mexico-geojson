import pandas as pd
import json

def load_geojson(geojson_path: str) -> dict:
    with open(geojson_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_colonias(colonias_path: str) -> pd.DataFrame:
    names = pd.read_csv(colonias_path)
    names.columns = [column.lower().strip() for column in names.columns]
    names = names[["cp", "colonia", "tipo", "municipio", "estado"]]
    names["cp"] = names["cp"].astype(str).str.zfill(5) #standarize dtype
    return names

def get_dict(colonias_df: pd.DataFrame, column: str = "colonia", as_list: bool = True) -> dict:
    grouped = (
    colonias_df.groupby("cp")[column]
    )
    if as_list:
        return grouped.apply(list).to_dict()
    else:
        return grouped.first().to_dict()

def insert_into_geojson(geojson: dict, 
                        properties_df: pd.DataFrame, 
                        property: str, 
                        property_name:str,
                        as_list: bool = True,
                        return_dict: bool = False
                        ) -> dict | None:

    cp_property_dict = get_dict(properties_df, property, as_list)

    for feature in geojson["features"]:

        cp = str(feature["properties"]["d_codigo"]).zfill(5)
        feature["properties"][property_name] = cp_property_dict.get(cp, [])
    if return_dict:
        return geojson

def save_geojson(geojson, save_path: str, **kwargs) -> None:
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, **kwargs)    