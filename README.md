# Contributors

- **Ignasi Fibla Figuerola** - [ignasi.fibla@estudiantat.upc.edu](mailto:ignasi.fibla@estudiantat.upc.edu)
- **Ferran González García** - [ferran.gonzalez.garcia@estudiantat.upc.edu](mailto:ferran.gonzalez.garcia@estudiantat.upc.edu)

For any questions or issues, please reach out to Ignasi or Ferran directly.

---

# Table of Contents

1. [Project Structure](#project-structure)
2. [Folder Structure](#folder-structure)
    - [data](#data)
    - [dataops](#dataops)
    - [models](#models)
    - [notebooks](#notebooks)
    - [src](#src)
    - [ui](#ui)
3. [Repository Files](#repository-files)
4. [How to Access the UI](#how-to-access-the-ui)

---

# Project Structure

This project is organized into several main folders, each with a specific purpose to facilitate data processing and analysis within the Data Backbone architecture.

## Folder Structure

- **`data`**: Contains raw and organized data files at various transformation stages.
  - **`landing`**: Stores raw data in its initial format, with two main subfolders:
    - **`persistent`**: Holds specific datasets, such as motor vehicle collision data, organized by data type (e.g., crashes, vehicles, etc.) in a persistent storage format.
    - **`temporal`**: Temporary data files used during the transformation or cleaning process before moving to other layers.

- **`dataops`**: Defines data operations and pipelines.
  - **`dataops.py`** and **`pipeline.py`**: Central scripts for setting up and running data transformation and processing pipelines. These scripts include logic to move data through different data layers.

- **`models`**: Stores data storage structures and data models.
  - **`data_models`**: Contains specific data models, like safety API response schemas.
  - **`storage`**: Defines data storage layers.
    - **`layers`**: Includes scripts that handle data transformations and movement across layers (`landing`, `trusted`, `formatted`, `exploitation`).

- **`notebooks`**: Contains Jupyter notebooks organized by data processing layer (`exploitation`, `formatted`, `landing`, `trusted`).
  - Each notebook provides specific analyses or transformations for data in its respective layer, serving for exploration, testing, and validation purposes.

- **`src`**: Source code for data processing components, organized by data layers.
  - **`exploitation`**: Data exploitation scripts focused on specific analyses, such as collision and vehicle information.
  - **`formatted`**: Scripts that format data into appropriate file types, such as CSV and JSON.
  - **`helpers`**: Utility scripts to facilitate data handling (database connectors, monitoring, CSV sampling).
  - **`landing`**: Initial processing for raw data, focusing on its integration into the database.
  - **`trusted`**: Cleansing and validation scripts to ensure data integrity before exploitation.

- **`ui`**: Streamlit-based user interface for interacting with the Data Backbone.
  - **`.streamlit`**: Streamlit configuration files.
  - **`pages`**: Contains UI modules for navigating different data layers.
  - **`profilings`**: Stores HTML files that provide detailed data profiles for each layer.
  - **`simulation`**: Simulated data files that mimic data inputs over different dates, stored in `landing/temporal`.

## Repository Files

- **`requirements.txt`**: Lists dependencies required to run the project.

## How to Access the UI

Follow these steps to execute and analyze all code in this first deliverable.

This project has been primarily executed locally, without the use of Google Colab or other third-party software. For simplicity, we recommend using the JetBrains IDE **PyCharm**, which was used throughout development, though other IDEs should work fine with the repository.

1. **Access the Repository**: Go to the following link: [https://github.com/IFibla/adsdb-project](https://github.com/IFibla/adsdb-project). This deliverable includes the repository with local files. You should be able to proceed smoothly. If any issues arise, please contact either Ignasi or Ferran.

2. **Install the Requirements**: Install dependencies by running the following command in your terminal:
   ```bash
   pip install -r requirements.txt
   ```
   Alternatively, you can manually install packages listed in **`requirements.txt`**.

2**Start the UI Server**: Start the Streamlit server by running:
    ```bash
    streamlit run ui/Hello.py
    ```
    This command will automatically open a webpage on a specified port, from which you can run the entire data pipeline and access additional documentation for the project.
   
