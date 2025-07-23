# CSV to Parquet Converter using Polars

This repository provides a Python-based tool for converting `.csv` files into `.parquet` format using the high-performance [Polars](https://www.pola.rs) library. It includes both a command-line version and a simple graphical user interface (GUI) implementation.

## 🔧 Features

- Automatically filters and converts only `.csv` files in the `data` directory
- Outputs `.parquet` files into the `parquet` folder
- Handles mixed file types (e.g., `.csv`, `.dat`) without manual filtering
- GUI version with file preview, progress bar, and threading for responsive performance

## 📁 Project Structure
```
project-root/
├── convert_csv_to_parquet.py # CLI version
├── csv_to_parquet_gui.py # GUI version using tkinter
├── data/ # Input directory (CSV files to convert)
│ ├── sample1.csv
│ ├── sample2.dat # Will be ignored
├── parquet/ # Output directory (converted Parquet files)
```

## 📦 Dependencies

- `polars`
- `tkinter` (standard with Python, for GUI)
- `os`, `threading`, `time` (built-in)

Install the required third-party package:

```bash
pip install polars
```

## 🚀 Usage
### CLI Version
```bash
python convert_csv_to_parquet.py
```
This will:

- Automatically read all .csv files in the data/ directory
- Convert them to .parquet format
- Save them into the parquet/ directory

### GUI Version
```bash
python csv_to_parquet_gui.py
```
The GUI version provides:

- File listing from data/ folder
- Real-time conversion progress
- Success/failure messages

## 📝 Notes
- The script processes only .csv files, even if other formats (e.g., .dat) are present in the data folder.
- The parquet/ directory will be created automatically if it does not exist.

## 📌 Example
If data/ contains:

```
data/
├── dataset1.csv
├── dataset2.csv
├── dataset3.dat
```
After execution, parquet/ will contain:

```
parquet/
├── dataset1.parquet
├── dataset2.parquet
```

## 📮 Contact
For questions or suggestions, please open an issue or contact @its-spark-dev.
