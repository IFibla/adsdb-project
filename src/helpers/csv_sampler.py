import pandas as pd


class CSVSampler:
    def __init__(self, input_file: str):
        """
        Initialize CSVSampler with the path to the input CSV file.

        :param input_file: Path to the large input CSV file.
        """
        self.input_file = input_file

    def random_sample(
        self, sample_size: int = 200, output_file: str = None
    ) -> pd.DataFrame:
        """
        Get a random sample of rows from the CSV file.

        :param sample_size: Number of rows to sample, default is 200.
        :param output_file: Optional path to save the sampled output CSV file.
        :return: A DataFrame containing the sampled rows.
        """
        sample_df = pd.read_csv(self.input_file).sample(n=sample_size, random_state=1)

        if output_file:
            sample_df.to_csv(output_file, index=False)
            print(f"Sample of {sample_size} rows saved to {output_file}")

        return sample_df

    def sort_and_sample(
        self, column_to_sort: str, sample_size: int = 200, output_file: str = None
    ) -> pd.DataFrame:
        sample_df = pd.read_csv(self.input_file)
        sample_df.sort_values(column_to_sort, ascending=False, inplace=True)
        sample_df = sample_df.iloc[0:sample_size]

        if output_file:
            sample_df.to_csv(output_file, index=False)
            print(f"Sample of {sample_size} rows saved to {output_file}")

        return sample_df

    def year_split(self, date_columns: str, output_directory: str):
        sample_df = pd.read_csv(self.input_file, parse_dates=[date_columns])

        sample_df["Year"] = sample_df[date_columns].dt.year

        for year, data in sample_df.groupby("Year"):
            if output_directory:
                data.to_csv(f"{output_directory}/{year}.csv", index=False)
                print(f"Sample of {len(data)} rows saved to {output_directory}")
