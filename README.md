# 🚕 Cab Management App

A **Streamlit**-based cab management application for IT companies. Manage vehicles, drivers, employee ride requests, trip assignments, and view dashboard analytics — all backed by **SQLite** via **SQLAlchemy**.

## Features

- **Vehicle Management** — Add, edit, view, and remove cabs/vehicles (registration number, model, capacity, status).
- **Driver Management** — Add, edit, view, and remove drivers (name, license number, phone, assigned vehicle).
- **Employee Ride Requests** — Employees can request a cab (pickup/drop location, date/time, purpose).
- **Trip Assignment & Tracking** — Assign a cab + driver to a request; mark trips as scheduled / in-progress / completed / cancelled.
- **Dashboard / Reporting** — Summary stats (total cabs, active trips, available drivers) and a simple trip history log.

## Tech Stack

| Layer       | Technology              |
|-------------|-------------------------|
| UI          | Streamlit               |
| ORM         | SQLAlchemy              |
| Database    | SQLite                  |
| Charts      | Plotly                  |
| Data        | Pandas                  |
| Testing     | pytest                  |

## Project Structure

```
cab-management-app/
├── app.py                  # Streamlit entry point
├── database/
│   ├── __init__.py
│   ├── db.py               # Engine, session factory, init_db()
│   └── models.py           # SQLAlchemy ORM models
├── pages/
│   ├── __init__.py
│   ├── dashboard.py        # Dashboard & reporting
│   ├── vehicles.py         # Vehicle management
│   ├── drivers.py          # Driver management
│   ├── requests.py         # Employee ride requests
│   └── trips.py            # Trip assignment & tracking
├── tests/
│   ├── __init__.py
│   └── test_models.py      # Model & DB tests
├── requirements.txt
├── .gitignore
└── .github/
    └── workflows/
        └── ci.yml          # CI pipeline — lint + test
```

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/mukundprasadhscl/cab-management-app.git
cd cab-management-app

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py

# 5. Run tests
pytest
```

## Environment

No external services required — the app uses a local SQLite database (`cab_management.db`) created automatically on first run.

## License

MIT
