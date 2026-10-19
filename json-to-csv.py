class JSONToCSVConverter:
    def __init__(self, filename, input_dir="json", output_dir="csv"):
        self.filename = filename
        self.input_dir = input_dir
        self.output_dir = output_dir

    def load_json_file(self):
        import os
        import json

        path = os.path.join(self.input_dir, self.filename)
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {path}")
            return None

    def convert_to_dataframe(self, data):
        import pandas as pd

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list) and value:
                    df = pd.json_normalize(value, sep="_")

                    if "transactions" in df.columns:
                        df = df.explode("transactions").reset_index(drop=True)
                        is_dict = df["transactions"].apply(lambda x: isinstance(x, dict))
                        txn_records = df.loc[is_dict, "transactions"].tolist()
                        if txn_records:
                            txn_df = pd.json_normalize(txn_records, sep="_").add_prefix("transaction_")
                            txn_df.index = df.index[is_dict]
                            df = df.drop(columns=["transactions"]).join(txn_df)
                        else:
                            df = df.drop(columns=["transactions"])

                    return df
        return pd.DataFrame()

    def save_to_csv(self, dataframe, filename):
        import os

        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, filename.replace('.json', '.csv'))
        dataframe.to_csv(output_file, index=False)
        print(f"Saved CSV to: {output_file}")

    def process_file(self):
        data = self.load_json_file()
        if data is None:
            return
        df = self.convert_to_dataframe(data)
        if not df.empty:
            self.save_to_csv(df, self.filename)
        else:
            print("No convertible data found (expected a dict containing a list).")


converter = JSONToCSVConverter("test.json")
converter.process_file()