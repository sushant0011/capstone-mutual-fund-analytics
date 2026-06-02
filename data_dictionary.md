# Data Dictionary — Bluestock Mutual Fund Analytics Database

This document details the database schemas, column data types, business definitions, and sources for the `bluestock_mf.db` Star Schema.

---

## 1. Table: `dim_fund`
Holds master profile details of the processed mutual fund schemes.
* **Source:** Derived dynamically from raw master datasets.

| Column Name | Data Type | Key Type | Business Definition |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | Primary Key | Unique 6-digit identification code provided by AMFI. |
| `scheme_name` | TEXT | None | Registered name of the mutual fund scheme. |
| `category` | TEXT | None | Broader classification asset class (e.g., Equity, Debt). |
| `sub_category` | TEXT | None | Specialized style classification (e.g., Large Cap, Mid Cap). |

---

## 2. Table: `fact_nav`
Stores time-series historical Net Asset Values (NAV) for analytical charting.
* **Source:** Cleaned output from `02_nav_history.csv`.

| Column Name | Data Type | Key Type | Business Definition |
| :--- | :--- | :--- | :--- |
| `nav_id` | INTEGER | Primary Key | Auto-incrementing identifier for every entry record. |
| `amfi_code` | INTEGER | Foreign Key | References `dim_fund(amfi_code)`. |
| `date` | TEXT | None | Valid trade calendar date (formatted as YYYY-MM-DD). |
| `nav` | REAL | None | Cleaned per-unit commercial asset value of the fund. |

---

## 3. Table: `fact_transactions`
Captures commercial business operations triggered by retail investors.
* **Source:** Cleaned output from `08_investor_transactions.csv`.

| Column Name | Data Type | Key Type | Business Definition |
| :--- | :--- | :--- | :--- |
| `transaction_id` | INTEGER | Primary Key | Unique tracking ID for each investor financial activity. |
| `amfi_code` | INTEGER | Foreign Key | References `dim_fund(amfi_code)`. |
| `investor_id` | INTEGER | None | Unique anonymous identification token for consumers. |
| `transaction_type` | TEXT | None | Enumerated activity labels (`SIP`, `Lumpsum`, `Redemption`). |
| `amount` | REAL | None | Aggregated transaction value computed in standard INR currency. |
| `transaction_date`| TEXT | None | Timestamp sequence record of the order execution. |
| `kyc_status` | TEXT | None | Operational regulatory status of user documentation. |
| `state` | TEXT | None | Geographic location origin point of the transaction request. |

---

## 4. Table: `fact_performance`
Stores return structures, structural administrative costs, and asset scales.
* **Source:** Cleaned output from `07_scheme_performance.csv`.

| Column Name | Data Type | Key Type | Business Definition |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | Primary Key / FK | Unique AMFI code referencing `dim_fund(amfi_code)`. |
| `one_year_return` | REAL | None | Totalized percentage gain structure across trailing 12 months. |
| `three_year_return`| REAL | None | Cumulative annual compounding returns across trailing 3 years. |
| `five_year_return` | REAL | None | Cumulative annual compounding returns across trailing 5 years. |
| `expense_ratio` | REAL | None | Yearly flat operational expense percentage cut (0.1% - 2.5%). |
| `aum` | REAL | None | Current Assets Under Management scale matrix valuation. |