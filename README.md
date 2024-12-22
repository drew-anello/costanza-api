# Costazna API 

## Overview

The Costazna API is a serverless application built with FastAPI and hosted on AWS Lambda. It provides famous quotes by George and Frank Costanza from the television show "Seinfeld".

## Features

- Fetch random quotes.
- Retrieve quotes by character (George or Frank Costanza).
- Retrieve Random quote by character (George or Frank).
- Fast and scalable API using AWS Lambda and FastAPI.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip package manager

## Usage

Access the following endpoints to interact with the API:

### API Endpoints

- `GET /getquotes/` - Retrieve all quotes.
- `GET /quote/random` - Retrieve a random quote.
- `GET /quotes/{character}` - Retrieve all quotes by character (`george` or `frank`).
- `GET /{character}/random` - Retrieve a random quote by character (`george` or `frank`).

Example:

```bash
curl https://costanza.vandelayindustries.biz/quotes/george
```
