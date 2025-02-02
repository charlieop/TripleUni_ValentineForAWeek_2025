import sqlite3
import pandas as pd
from pandas import DataFrame
from typing import Tuple


def connect_db_and_get_table(path: str, table_name: str) -> pd.DataFrame:
    """
    Connects to a SQLite database and retrieves all data from the specified table.

    Args:
        path (str): The file path to the SQLite database.
        table_name (str): The name of the table to retrieve data from.

    Returns:
        pd.DataFrame: A pandas DataFrame containing all data from the specified table.
    """
    db = sqlite3.connect(path)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    datas = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    db.close()
    return pd.DataFrame(datas, columns=columns)


def filter_applicant(data: DataFrame) -> DataFrame:
    """
    Filters out applicants who have either quit or are marked for exclusion.
    Args:
        data (DataFrame): The input DataFrame containing applicant data. 
                          It must have columns "quitted" and "exclude" with boolean values.
    Returns:
        DataFrame: A DataFrame containing only the applicants who have not quit and are not marked for exclusion.
    """
    if "quitted" in data.columns and "exclude" in data.columns:
        return data[(data["quitted"] == 0) & (data["exclude"] == 0)]
    else:
        raise KeyError("Columns 'quitted' and 'exclude' must be present in the DataFrame")


def separate_groups(data: DataFrame) -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    """
    Separates the input DataFrame into four groups based on sex and preferred sex.

    Args:
        data (DataFrame): The input DataFrame containing user data with at least two columns: 
                          'sex' and 'preferred_sex'.

    Returns:
        Tuple[DataFrame, DataFrame, DataFrame, DataFrame]: A tuple containing four DataFrames:
            - heterosexual_female_list: Users who are female and prefer males.
            - heterosexual_male_list: Users who are male and prefer females.
            - homosexual_female_list: Users who are female and prefer females.
            - homosexual_male_list: Users who are male and prefer males.
    """
    heterosexual_female_list = data[(data["sex"] == "F") & (data["sex"] != data["preferred_sex"])].reset_index(drop=True)
    heterosexual_male_list = data[(data["sex"] == "M") & (data["sex"] != data["preferred_sex"])].reset_index(drop=True)
    homosexual_female_list = data[(data["sex"] == "F") & (data["sex"] == data["preferred_sex"])].reset_index(drop=True)
    homosexual_male_list = data[(data["sex"] == "M") & (data["sex"] == data["preferred_sex"])].reset_index(drop=True)
    return heterosexual_female_list, heterosexual_male_list, homosexual_female_list, homosexual_male_list


def reshuffle_data(data: DataFrame) -> DataFrame:
    """
    Reshuffles the input DataFrame to ensure that the data is not sorted by any column.
    """
    return data.sample(frac=1).reset_index(drop=True)