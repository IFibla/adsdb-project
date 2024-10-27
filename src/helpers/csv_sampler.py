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
