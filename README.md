
# 🎬 Future Mind – Data Warehouse Project

## 🎯 1. Project Goal

Build a complete data warehouse pipeline that:

- 📥 Ingests daily movie revenue data from a CSV file
- 🔎 Enriches movie metadata via the OMDb API
- 🏗 Loads data into an Oracle-based dimensional model:
  - `DIM_DISTRIBUTORS`, `DIM_MOVIES`, `FACT_REVENUE`
- ☁️ Exports aggregated data to BigQuery
- 📊 Visualizes insights in Looker Studio (GCP)

---

## 📊 2. Final Dashboard

[👉 View the Dashboard in Looker Studio](https://lookerstudio.google.com/s/qP_Y-6GnQX8)

Contains:

- 🏆 Top distributors by revenue
- 🎬 Top movie titles by revenue
- 📈 Revenue trend by year

Styled in dark mode with pastel chart colors 🌙🎨

---

## 🧠 3. Technologies Used

- Python 3.12+ 🐍
- Oracle Database XE 21c (locally) 🧱
- OMDb API 🎥
- Google BigQuery & Looker Studio ☁️
- Poetry & Makefile 🛠

---

## 📁 4. Project Structure

```
futuremind_data_warehouse/
├── data/                         # CSV files
├── src/
│   ├── pipeline/                 # Oracle Loaders
│   │   ├── distributor_loader.py
│   │   ├── movie_loader.py
│   │   └── fact_revenue_loader.py
│   ├── utils/
│   │   └── omdb_client.py
│   └── oracle_connection.py
├── tests/
├── .env                          # Env credentials (not in Git)
├── Makefile                      # Shortcut commands
├── pyproject.toml                # Poetry config
└── README.md                     # This file
```

---

## ⚙️ 5. Setup Instructions

### 5.1 Clone the repo

```bash
git clone https://github.com/KedarSki/futuremind_data_warehouse.git
cd futuremind_data_warehouse
```

### 5.2 Install dependencies

```bash
poetry install
```

### 5.3 Activate virtual environment

```bash
poetry shell
```

### 5.4 Create a `.env` file

```ini
OMDB_API_KEY=your_api_key
ORACLE_USERNAME=future_mind_user
ORACLE_PASSWORD=your_password
ORACLE_DSN=localhost/XEPDB1
CSV_PATH=C:/Git/futuremind_data_warehouse/data/revenues_per_day.csv
```

---

## 🛠️ 6. Running the Pipeline

### 6.1 Create schema and tables in Oracle

```sql
CREATE USER future_mind_user IDENTIFIED BY your_password;
GRANT CONNECT, RESOURCE TO future_mind_user;

-- Dimension Tables
CREATE TABLE DIM_DISTRIBUTORS (...);
CREATE TABLE DIM_MOVIES (...);

-- Fact Table
CREATE TABLE FACT_REVENUE (...);
```

### 6.2 Run loaders

```bash
make run-distributors     # Step 1
make run-movies           # Step 2
make run-facts            # Step 3
```

or:

```bash
python main.py            # Full pipeline
```

---

## ☁️ 7. GCP Dashboard

Exported Oracle data to BigQuery → view `vw_revenue_report`

Connected to Looker Studio for visualization.

### View columns:

- DISTRIBUTOR_NAME
- TITLE, GENRE, DIRECTOR, YEAR
- REVENUE, REVENUE_DATE, THEATERS

---

## 🧪 8. Code Quality

```bash
make check-all   # Black + Pylint + Mypy + Tests
```

---

## 👤 9. Author

**Radosław Zamojski**  
🇵🇱 Poland  
🔗 [GitHub](https://github.com/KedarSki)  
🔗 [LinkedIn](https://www.linkedin.com/in/radoslaw-zamojski/)
