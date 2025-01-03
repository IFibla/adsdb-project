from typing import Dict, List, Tuple, Union
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import pandas as pd
import numpy as np
import os


class DataProfiler:
    """
    Generates a profiling report from a given pandas DataFrame.

    This class calculates various descriptive statistics, identifies data types,
    detects missing values, computes correlations, and generates visualizations
    to provide a comprehensive overview of the input DataFrame.
    It does NOT use pandas_profiling.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initializes the DataProfiler with a pandas DataFrame.

        Args:
            df: The pandas DataFrame to profile.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        self.df = df
        self.profile_results = {}

    def calculate_descriptive_stats(self) -> Dict[str, pd.DataFrame]:
        """
        Calculates descriptive statistics for numerical and categorical columns.

        Returns:
            A dictionary where keys are 'numerical' and 'categorical', and values
            are DataFrames containing descriptive statistics for the respective
            column types.
        """
        numerical_stats = self.df.describe(include=[np.number])
        categorical_stats = self.df.describe(include=["object"])

        return {"numerical": numerical_stats, "categorical": categorical_stats}

    def identify_data_types(self) -> pd.Series:
        """
        Identifies the data type of each column in the DataFrame.

        Returns:
            A pandas Series where the index is the column names and the values are
            the corresponding data types.
        """
        return self.df.dtypes

    def detect_missing_values(self) -> pd.DataFrame:
        """
        Calculates the number and percentage of missing values for each column.

        Returns:
            A pandas DataFrame with columns 'missing_count' and 'missing_percentage'
            representing the number and percentage of missing values, respectively.
        """
        missing_count = self.df.isnull().sum()
        missing_percentage = (missing_count / len(self.df)) * 100
        return pd.DataFrame(
            {"missing_count": missing_count, "missing_percentage": missing_percentage}
        )

    def calculate_correlations(self) -> pd.DataFrame:
        """
        Calculates the pairwise correlation between numerical columns.

        Returns:
            A pandas DataFrame representing the correlation matrix.
        """
        return self.df.corr(numeric_only=True)

    def generate_histograms(
        self, numerical_columns: List[str], output_dir: str = "histograms"
    ):
        """
        Generates histograms for specified numerical columns.

        Args:
            numerical_columns: A list of numerical column names for which to generate histograms.
            output_dir: The directory to save the histogram plots. Defaults to "histograms".
        """
        os.makedirs(output_dir, exist_ok=True)

        for col in numerical_columns:
            if col in self.df.columns and pd.api.types.is_numeric_dtype(self.df[col]):
                plt.figure()
                sns.histplot(self.df[col], kde=True)
                plt.title(f"Histogram of {col}")
                plt.savefig(f"{output_dir}/{col}_histogram.png")
                plt.close()

    def generate_bar_plots(
        self, categorical_columns: List[str], output_dir: str = "barplots"
    ):
        """
        Generates bar plots for specified categorical columns.

        Args:
            categorical_columns: A list of categorical column names for which to generate bar plots.
            output_dir: The directory to save the bar plots. Defaults to "barplots".
        """
        os.makedirs(output_dir, exist_ok=True)

        for col in categorical_columns:
            if col in self.df.columns and pd.api.types.is_object_dtype(self.df[col]):
                plt.figure()
                sns.countplot(x=col, data=self.df)
                plt.title(f"Bar plot of {col}")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                plt.savefig(f"{output_dir}/{col}_barplot.png")
                plt.close()

    def detect_outliers(
        self, numerical_columns: List[str], method: str = "iqr"
    ) -> Dict[str, List[int]]:
        """
        Detects outliers in numerical columns using either IQR or Z-score method.

        Args:
            numerical_columns: A list of numerical column names for outlier detection.
            method: The method for outlier detection ('iqr' or 'zscore'). Defaults to 'iqr'.

        Returns:
            A dictionary where keys are column names and values are lists of indices
            corresponding to outlier data points in each column.
        """
        outliers_dict = {}

        for col in numerical_columns:
            if col in self.df.columns and pd.api.types.is_numeric_dtype(self.df[col]):
                if method == "iqr":
                    Q1 = self.df[col].quantile(0.25)
                    Q3 = self.df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = self.df.index[
                        (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
                    ].tolist()

                elif method == "zscore":
                    z_scores = np.abs(stats.zscore(self.df[col]))
                    outliers = self.df.index[z_scores > 3].tolist()

                else:
                    raise ValueError("Invalid method. Choose 'iqr' or 'zscore'.")

                outliers_dict[col] = outliers

        return outliers_dict

    def generate_report(self, output_file: str = "data_profile.txt"):
        """
        Generates a comprehensive text-based profiling report.

        Args:
            output_file: The path to the output text file. Defaults to "data_profile.txt".
        """
        self.profile_results["descriptive_stats"] = self.calculate_descriptive_stats()
        self.profile_results["data_types"] = self.identify_data_types()
        self.profile_results["missing_values"] = self.detect_missing_values()
        self.profile_results["correlations"] = self.calculate_correlations()

        numerical_columns = self.df.select_dtypes(include=np.number).columns.tolist()
        categorical_columns = self.df.select_dtypes(include=["object"]).columns.tolist()

        self.generate_histograms(numerical_columns)
        self.generate_bar_plots(categorical_columns)

        self.profile_results["outliers"] = self.detect_outliers(numerical_columns)

        with open(output_file, "w") as f:
            f.write("Data Profiling Report\n")
            f.write("====================\n\n")

            f.write("1. Data Types:\n")
            f.write(self.profile_results["data_types"].to_string() + "\n\n")

            f.write("2. Descriptive Statistics:\n")
            for stats_type, stats_df in self.profile_results[
                "descriptive_stats"
            ].items():
                f.write(f"\n{stats_type.capitalize()}:\n")
                f.write(stats_df.to_string() + "\n")

            f.write("\n3. Missing Values:\n")
            f.write(self.profile_results["missing_values"].to_string() + "\n\n")

            f.write("4. Correlations:\n")
            f.write(self.profile_results["correlations"].to_string() + "\n\n")

            f.write("5. Outliers (using IQR):\n")
            for col, outlier_indices in self.profile_results["outliers"].items():
                f.write(f"Column: {col}\n")
                if outlier_indices:
                    f.write(f"Outlier indices: {outlier_indices}\n")
                else:
                    f.write("No outliers detected.\n")
            f.write("\n")

            f.write("6. Visualizations:\n")
            f.write("- Histograms generated and saved to 'histograms' directory.\n")
            f.write("- Bar plots generated and saved to 'barplots' directory.\n")

        print(f"Profiling report generated and saved to: {output_file}")
