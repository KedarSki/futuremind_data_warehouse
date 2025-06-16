# Future Mind - Data Warehouse Project

## 🎯 Project Goal

Build a data warehouse pipeline that:

* Ingests daily movie revenue data from a CSV file
* Enriches the data with metadata from the OMDb API
* Loads the data into a dimensional Oracle data model:

  * 1 fact table: `FACT_REVENUE`
  * 2 dimension tables: `DIM_MOVIES`, `DIM_DISTRIBUTORS`
* \[WIP] Uploads the result to BigQuery with a dashboard in Looker Studio

---

## 📁 Project Structure

```
futuremind_data_warehouse/
├── data/                            # CSV files (original + processed)
├── src/
│   ├── pipeline/                    # Loaders for Oracle
│   │   ├── distributor_loader.py
│   │   ├── movie_loader.py
│   │   └── fact_revenue_loader.py
│   ├── utils/
│   │   └── omdb_client.py          # OMDb API handler
│   └── oracle_connection.py        # Context-managed Oracle connector
├── .env                            # Environment variables (excluded from Git)
├── Makefile                        # Command shortcuts
├── pyproject.toml                  # Poetry project config
└── README.md                       # This file
```

---

## ⚙️ Requirements

* Python 3.12+
* [Oracle Database XE](https://www.oracle.com/database/technologies/xe-downloads.html)
* [Poetry](https://python-poetry.org/)

---

## ▶️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourname/futuremind_data_warehouse.git
cd futuremind_data_warehouse
```

### 2. Install dependencies

```bash
poetry install
```

### 3. Activate environment

```bash
poetry shell
```

### 4. Prepare `.env` file

Create `.env` in the root folder:

```
OMDB_API_KEY=your_omdb_key
ORACLE_USERNAME=future_mind_user
ORACLE_PASSWORD=your_password
ORACLE_DSN=localhost/XEPDB1
```

---

## 🛠️ Makefile commands

```bash
make distributors     # Load unique distributors into Oracle
make movies           # Load movie data from OMDb into Oracle
make revenue          # Load fact table with revenue per day
```

You can chain them via:

```bash
make all              # Full pipeline
```

---

## 🗄️ Oracle Setup (local)

### 1. Create user & schema

Run in SQL\*Plus or DBeaver:

```sql
CREATE USER future_mind_user IDENTIFIED BY your_password;
GRANT CONNECT, RESOURCE TO future_mind_user;
ALTER USER future_mind_user DEFAULT TABLESPACE users;
```

### 2. Create tables (if needed)

```sql
-- Dimension: distributors
CREATE TABLE DIM_DISTRIBUTORS (
  DISTRIBUTOR_ID VARCHAR2(36) PRIMARY KEY,
  NAME VARCHAR2(255)
);

-- Dimension: movies
CREATE TABLE DIM_MOVIES (
  MOVIE_ID VARCHAR2(36) PRIMARY KEY,
  TITLE VARCHAR2(255),
  YEAR NUMBER,
  GENRE VARCHAR2(255),
  DIRECTOR VARCHAR2(255)
);

-- Fact: revenue
CREATE TABLE FACT_REVENUE (
  ID VARCHAR2(36) PRIMARY KEY,
  MOVIE_ID VARCHAR2(36),
  DISTRIBUTOR_ID VARCHAR2(36),
  REVENUE_DATE DATE,
  REVENUE NUMBER,
  THEATERS VARCHAR2(255),
  FOREIGN KEY (MOVIE_ID) REFERENCES DIM_MOVIES(MOVIE_ID),
  FOREIGN KEY (DISTRIBUTOR_ID) REFERENCES DIM_DISTRIBUTORS(DISTRIBUTOR_ID)
);
```

---

## ☁️ GCP Integration \[coming soon]

A separate branch or update will include:

* Export to BigQuery
* Hosting in GCP with Looker Studio dashboard

ETA: 1 day after submission of this version.

---

## 📬 Contact

Radoslaw Zamojski
[GitHub](https://github.com/KedarSki)
[LinkedIn](https://www.linkedin.com/in/radoslaw-zamojski/)
