import json
import sys
import pandas as pd

# noinspection SpellCheckingInspection
EXAMPLE_CTRL_JSON = """######### EXAMPLE JSON: #########
{
    "save_path": "./basic_stat.csv", 
    "data": [
        {
            "name": "Baseline", 
            "csv_path": "./similarity_score.csv", 
            "col_name": "baseline",
            "invalid_cell_as": 0,
        }, 
        {
            "name": "Tor", 
            "csv_path": "./similarity_score.csv", 
            "col_name": "torsocks",
            "invalid_cell_as": 0,
        }
    ]
}
"""


def data_prepare(df_path, col_name, invalid_cell_as=None):
    """
    sample_range = [start, end, interval], start can be left, end can be right if all data are included.
    """
    df = pd.read_csv(df_path)
    df = df[col_name]
    if invalid_cell_as is not None:
        df = df.fillna(float(invalid_cell_as))
    return df


def describe(df):
    res = dict(df.describe())
    res["median"] = df.median()
    return res


def parse_cmd(json_path):
    with open(json_path, 'r') as f:
        commands = json.load(f)
    result = []
    for data_single in commands['data']:
        if "invalid_cell_as" in data_single:
            invalid_cell_as = data_single['invalid_cell_as']
        else:
            invalid_cell_as = None
        raw_data = data_prepare(data_single['csv_path'], data_single['col_name'],
                                invalid_cell_as=invalid_cell_as)
        res = describe(raw_data)

        res['name'] = data_single['name']
        print(res)
        result.append(res)
    df = pd.DataFrame(result)
    df[["name", "mean", "median", "std"]].to_csv(commands["save_path"], index=False)
    print(df[["name", "mean", "median", "std"]])


def generate_example_json():
    print(EXAMPLE_CTRL_JSON)


def main():
    if len(sys.argv) != 2:
        print("Usage: basic_stat path/to/conf.json")
        exit()
    if sys.argv[1] == '-g':
        generate_example_json()
    else:
        parse_cmd(sys.argv[1])


if __name__ == '__main__':
    main()
