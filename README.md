# Vacation Budget Estimator

A database course project: estimates total vacation cost (flight + hotel) for
a traveler departing Israel, by integrating two independent public data
sources that key destinations in incompatible ways.

## Data sources

- **Flights**: [Travelpayouts Data API](https://travelpayouts-data-api.readthedocs.io/) (`v3/prices_for_dates`) -- cached real-user round-trip searches by IATA origin/destination + month. Live, collected repeatedly by running the collector manually -- this is the project's time-series data.
- **Hotels**: [SerpApi's Google Hotels API](https://serpapi.com/google-hotels-api) -- a live current-price quote per destination (free tier: 250 searches/month, run manually, not on cron). *(Originally planned against the live Hotellook API, which shut down permanently on 2025-10-15 -- confirmed via Travelpayouts' own support docs. A static CSV (Gabor's Data Analysis "hotels-europe" dataset) was used as a temporary stopgap, then removed entirely once SerpApi was found and gave full coverage across all 45 destinations with no city-name-matching problem.)*
- **Airports**: a small curated subset (not the full OurAirports dump) of real IATA airport data.

See `report/report.md` for the full write-up.

## Setup

1. **Start Postgres**: `docker run -d --name vacation_budget_db -e POSTGRES_USER=vacation -e POSTGRES_PASSWORD=<choose_a_password> -e POSTGRES_DB=vacation_budget -p 5432:5432 postgres:16` (or `docker compose up -d` if your Docker install has the compose plugin). Pick your own password for `POSTGRES_PASSWORD` and use the same value in `DB_URL` in your `.env` (see step 3).
2. **Install dependencies**: `pip install --user -r requirements.txt` (or use a venv if `python3-venv` is installed).
3. **Configure secrets**: `cp .env.example .env`, then register for a free token at
   https://www.travelpayouts.com/programs/100/tools/api and fill in `TRAVELPAYOUTS_TOKEN`
   (and `TRAVELPAYOUTS_MARKER`, from the same dashboard). This is only needed for flights now.
4. **Apply schema**: `python3 -m etl.loaders.run_migrations`
5. **Load reference data**:
   ```
   python3 -m etl.loaders.load_airports
   python3 -m etl.loaders.load_destinations_seed
   python3 -m etl.loaders.refresh_exchange_rates
   ```
6. **Load hotel prices**: register free at https://serpapi.com and fill in `SERPAPI_KEY` in `.env`, then `python3 -m etl.collectors.hotels_collector` (queries all active destinations -- mind the 250 searches/month free-tier cap, see that module's docstring).
7. **Run the flight collector, repeatedly:**
   ```
   python3 -m etl.collectors.flights_collector
   ```
   The schema is designed around daily snapshots collected over several weeks; this
   project's actual collection window was compressed to a few days due to the course
   timeline (see `report/report.md` for the disclosed scale). Each run adds a fresh
   `observed_at` snapshot -- it never overwrites, so running it repeatedly builds up
   real time-series data.
8. **Run the app**: `python3 -m flask --app app.main run --debug`, then visit http://127.0.0.1:5000

## Tests

`python3 -m pytest tests/ -v` -- currency conversion tests run standalone; query-shape
tests require the dev database to be up and migrated/seeded (they skip automatically
otherwise).
