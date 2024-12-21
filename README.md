# Tax Return Estimator (TRE)

Tax Return Estimator (TRE) is a Python-based application designed to help individuals and organizations calculate tax liabilities and returns. The project demonstrates a 3-tiered architecture with communication between multiple components, including client applications, servers, and a database backend.

## Features
- Estimate tax returns based on taxable income or net wages.
- Support for different tax scenarios, including private health insurance and Medicare Levy.
- Handles cases with and without a Tax File Number (TFN).
- Persistent storage and retrieval of payroll records via a SQL database.
- Flexible configuration for local and remote server setups.

---

## Table of Contents
- [Tax Return Estimator (TRE)](#tax-return-estimator-tre)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Technologies Used](#technologies-used)
  - [System Design](#system-design)
  - [Setup and Installation](#setup-and-installation)
    - [Prerequisites](#prerequisites)
  - [Usage](#usage)
    - [TRE Client (tre\_client.py)](#tre-client-tre_clientpy)
    - [PTC Client (ptc\_client.py)](#ptc-client-ptc_clientpy)
    - [Example Session (TRE Client)](#example-session-tre-client)

---

## Technologies Used
- **Programming Language**: Python
- **Distributed Computing**: [Pyro4](https://pyro4.readthedocs.io/)
- **Database**: Microsoft SQL Server
- **Libraries**:
  - `pyodbc` for database connectivity
  - `Pyro4` for Remote Method Invocation (RMI)

---

## System Design
The project uses a **3-tier architecture**:
1. **Presentation Tier**: 
   - Clients (`tre_client.py`, `ptc_client.py`) for interacting with users and collecting input data.
2. **Application Tier**: 
   - Servers (`server-1.py`, `server-2.py`) to process tax calculation logic and interact with the database.
3. **Data Tier**: 
   - SQL Server for storing and retrieving payroll and tax data.

---

## Setup and Installation

### Prerequisites
- Python 3.9+
- SQL Server with the required schema (see `payroll_populate.sql` and `persons_populate.sql` for sample data).
- [Pyro4](https://pyro4.readthedocs.io/en/stable/) library:
  ```bash
  pip install Pyro4


## Usage
### TRE Client (tre_client.py)
- Used to estimate taxes for individuals.
- Prompts user for input such as TFN status, wages, and private health insurance.

### PTC Client (ptc_client.py)
- Used to calculate payroll taxes for employees.
- Allows adding payroll data to the database.

### Example Session (TRE Client)
1. Start the client and connect to the application server.
2. Input your details (TFN status, wages, etc.).
3. View the tax return estimate and other details.