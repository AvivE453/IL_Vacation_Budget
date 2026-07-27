-- Hotel-price reference data, one row per city, live via SerpApi's Google
-- Hotels API (etl/collectors/hotels_collector.py). Latest-snapshot-per-city
-- not append-only like flight_price_observations 
-- SerpApi's 250 searches/month cap rules out repeated snapshots (for free)
--
-- avg/luxury tier columns: average of the cheapest/priciest ~10 hotels in
-- the sample, alongside the plain average, so the app can offer a
-- budget/average/luxury choice. Nullable - too small a sample to split
-- means missing data, not a zero.

CREATE TABLE hotel_prices (
    hotel_price_id             SERIAL PRIMARY KEY,
    city_name_raw              TEXT NOT NULL,
    city_name_normalized       TEXT NOT NULL UNIQUE,
    avg_price_per_night_usd    NUMERIC(10,2) CHECK (avg_price_per_night_usd > 0),
    min_price_per_night_usd    NUMERIC(10,2) CHECK (min_price_per_night_usd > 0),
    sample_size                INTEGER NOT NULL CHECK (sample_size > 0),
    avg_price_budget_tier_usd  NUMERIC(10,2) CHECK (avg_price_budget_tier_usd > 0),
    avg_price_luxury_tier_usd  NUMERIC(10,2) CHECK (avg_price_luxury_tier_usd > 0),
    loaded_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);
