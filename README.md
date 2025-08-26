# Software Engineer Take-Home Project - Ertugrul Sert

## Objective
This project assesses the ability to evolve a proof-of-concept scraper into a robust, production-ready data pipeline.  
The goal is to reliably scrape job postings from a mock API, normalize and validate the data, and store it for later analysis.

---

## Running the Scraper

1. **Ensure the Mock API Server is Running**

The scraper relies on the mock API server. Start it with Docker:

docker compose up

## Verify Server 
- ** python test_api_connection.py **

## Running the Scraper

- python -m src.swe.scraper

- **The scraper will:**

- Fetch all companies.

- Retrieve jobs for each company (with retries and pagination).

- Normalize and validate data.

- Save all jobs to jobs.json.

- **After completion, jobs.json contains: ** 

- Job ID

- Job title

- Number of applicants

- Location (city, state, country)

- Posted date (ISO 8601)

## Example Summary (from a successful run)

=== SUMMARY ===

- Total number of companies processed: 5000

- Total jobs stored: 82386

- Total applicants counted: 5904327

- Total API requests made: 11203

- Total time: 2536.78s


## Testing Instructions

The project includes comprehensive tests for the scraper and in-memory database. Tests cover:

- **InMemoryDB functionality:** insertion, upsert, clearing, saving/loading from file.
- **Data normalization:** location parsing, posted date parsing, default values for missing fields.
- **API client behavior:** pagination handling, data normalization wrapping.

### Running the Tests

1. Make sure you have `pytest` installed. If not, install it with:

pip install pytest

### 
pytest -v test.py

## Architectural Decisions

- **Concurrency:** Used `ThreadPoolExecutor` to fetch multiple companies in parallel, improving throughput.
- **Retry & Error Handling:** Each API request retries up to 3 times for robustness.
- **Data Normalization:** 
  - Location strings and dictionaries are normalized to a consistent `Location` object.
  - Dates are normalized to ISO 8601 (`YYYY-MM-DD`) using UTC timestamps.
- **Data Persistence:** Jobs are first stored in-memory (`InMemoryDB`) and then persisted to a JSON file using `save_to_file`.
- **Pagination Handling / Next Page:** The scraper automatically follows `nextPageToken` in API responses, fetching up to 10 pages per company. This ensures all jobs are collected without risking infinite loops.
- **Configurable:** Number of threads and API base URL are easily adjustable via constants in the script.
- **Production Readiness Considerations:** 
  - Timeout values are set for network calls.
  - Thread pool size is configurable for different environments.
  - Failures in one company do not block processing of others.

## Completed Work vs. Not Done

### Completed
- Refactored scraper to be production-ready.
- Implemented data normalization for locations and dates.
- Implemented retries and error handling for API requests.
- Added pagination handling (`nextPageToken`) with a limit of 10 pages per company.
- Implemented in-memory database (`InMemoryDB`) and saving to JSON.
- Added multi-threading to fetch multiple companies concurrently.
- Wrote comprehensive tests using `pytest`


### Not Done / Pending
- Persistent relational database (currently only JSON storage).
- Exponential backoff for retry logic.
- Advanced logging instead of print statements.
- Automatic handling of API rate-limiting beyond retries.

---

## Known Limitations and Bugs

- Pagination limited to 10 pages per company; some jobs might not be captured if more pages exist.
- Timestamp normalization assumes UTC, which may not reflect original local times.
- If an API request fails after max retries, remaining pages for that company are skipped.
- JSON storage is not optimized for very large datasets.
- No strict schema validation beyond normalization; malformed API data could cause issues.

---

## Next Steps / Improvements

1. **Database Persistence**: Move from JSON to a relational database (PostgreSQL/SQLite/MongoDB) to support queries and reporting.
2. **Enhanced Retry Logic**: Implement exponential backoff and jitter for more robust handling of API rate limits.
4. **Logging and Monitoring**: Replace `print` statements with a configurable logging system, possibly with log levels (INFO, WARN, ERROR).
5. **Schema Validation**: Integrate strict validation of API response data using `pydantic` models or JSON Schema.
