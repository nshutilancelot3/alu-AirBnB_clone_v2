# AirBnB Clone - MySQL (v2)

A full-stack web application clone of AirBnB, built with Python and MySQL.

## Description

This project is an extension of the AirBnB clone that adds MySQL database storage via SQLAlchemy ORM, alongside the existing file-based storage system. Both storage engines can be switched using environment variables.

## Team

- **NYIRIHIRWE Yves**
- **Nshuti Lancelot**

## Original Authors

See [AUTHORS](./AUTHORS) file.

## Features

- Interactive command interpreter (console)
- Two storage engines:
  - **FileStorage**: stores objects in a JSON file
  - **DBStorage**: stores objects in a MySQL database via SQLAlchemy
- Object-Relational Mapping (ORM) with SQLAlchemy
- Unit tests for all components

## Environment Variables

| Variable | Description |
|---|---|
| `HBNB_ENV` | Running environment: `dev` or `test` |
| `HBNB_MYSQL_USER` | MySQL username |
| `HBNB_MYSQL_PWD` | MySQL password |
| `HBNB_MYSQL_HOST` | MySQL host (default: `localhost`) |
| `HBNB_MYSQL_DB` | MySQL database name |
| `HBNB_TYPE_STORAGE` | Storage type: `file` or `db` |

## Usage

### File Storage (default)
```bash
./console.py
```

### Database Storage
```bash
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd \
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db \
HBNB_TYPE_STORAGE=db ./console.py
```

### Console Commands
- `create <Class> [key=value ...]` — Create a new object
- `show <Class> <id>` — Show an object
- `destroy <Class> <id>` — Delete an object
- `all [Class]` — List all objects (optionally filtered by class)
- `update <Class> <id> <attr> <value>` — Update an attribute
- `count <Class>` — Count instances of a class
- `quit` / `EOF` — Exit the console

## MySQL Setup

```bash
# Development database
cat setup_mysql_dev.sql | mysql -hlocalhost -uroot -p

# Test database
cat setup_mysql_test.sql | mysql -hlocalhost -uroot -p
```

## Running Tests

```bash
# FileStorage
python3 -m unittest discover tests

# DBStorage
HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd \
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db \
HBNB_TYPE_STORAGE=db python3 -m unittest discover tests
```

## Models

| Class | Table | Description |
|---|---|---|
| State | states | Geographic state |
| City | cities | City within a state |
| User | users | Application user |
| Place | places | Rental listing |
| Review | reviews | Review of a place |
| Amenity | amenities | Amenity offered by a place |

## Requirements

- Python 3.8.5
- MySQL 8.0
- SQLAlchemy 1.4.x
- MySQLdb (mysqlclient)
- pycodestyle 2.7.*
