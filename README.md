# PDD Bot

A project for managing courses, subjects, students, assessments, and performance data.

## Requirements

- Python 3.8+
- PostgreSQL
- `pip` (Python package manager)

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/pdd_bot.git
cd pdd_bot
```

### 2. Install Python Dependencies

```sh
pip install -r requirements.txt
```

If `requirements.txt` does not exist, manually install:

```sh
pip install psycopg2 pandas python-dotenv
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```sh
cp .env.example .env
```

Edit `.env` and set:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
FENIX_USERNAME=...
FENIX_PASSWORD=...
FENIX_URL=...
...
```

### 4. Set Up the Database

1. **Create the database and user** (if not already done):

   ```sh
   psql -U postgres
   CREATE DATABASE your_db_name;
   CREATE USER your_db_user WITH PASSWORD 'your_db_password';
   GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
   ```

2. **Run the SQL scripts** in [`database scripts/`](database%20scripts/) in the following order:

   - `creation.sql`
   - `bd_user.sql`
   - `curso_functions.sql`
   - `cadeira_functions.sql`
   - `estudante_functions.sql`
   - `avaliacao_functions.sql`
   - `performance_functions.sql`
   - `test.sql` (optional, for testing)

   Example:

   ```sh
   psql -U your_db_user -d your_db_name -f "database scripts/creation.sql"
   psql -U your_db_user -d your_db_name -f "database scripts/bd_user.sql"
   psql -U your_db_user -d your_db_name -f "database scripts/curso_functions.sql"
   psql -U your_db_user -d your_db_name -f "database scripts/cadeira_functions.sql"
   psql -U your_db_user -d your_db_name -f "database scripts/estudante_functions.sql"
   psql -U your_db_user -d your_db_name -f "database scripts/avaliacao_functions.sql"
   psql -U your_db_user -d your_db_name -f "database scripts/performance_functions.sql"
   # Optional, for testing:
   psql -U your_db_user -d your_db_name -f "database scripts/test.sql"
   ```

### 5. Running the Application

You can run the main scripts as needed, for example:

```sh
python store_on_db.py
```

This will process and store data from Excel files into the database.

### 6. Backup

A backup script is provided in [`backup_script/backup.sh`](backup_script/backup.sh). Edit the script to set the correct paths and credentials.

---

## Folder Structure

- `service/` — Service layer for database operations
- `database scripts/` — SQL scripts for schema and functions
- `files/` — Data files (Excel, etc.)
- `backup_script/` — Database backup utilities

---

## Troubleshooting

- Ensure PostgreSQL is running and accessible.
- Check your `.env` file for correct credentials.
- Review logs for error messages.

---

## License

MIT License