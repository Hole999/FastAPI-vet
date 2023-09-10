# RestAPI Veterinary Management API

## Introduction

The RestAPI Veterinary Management API is a RESTful web service designed to help veterinary clinics manage animal records, treatments, and vets. It provides a secure and efficient way to perform CRUD (Create, Read, Update, Delete) operations on animals, treatments, and vet accounts.

This README provides essential information for setting up, running, and using the API.

## Features

- **Authentication and Authorization:** Secure endpoints using OAuth2 and JWT tokens.
- **Vet Management:** Register, authenticate, delete, and update vet accounts.
- **Animal Management:** Create, retrieve, update, and delete animal records.
- **Treatment Management:** Add, retrieve, update, and delete treatment records for animals.

## Requirements

- Python 3.7+
- MongoDB
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Hole999/RestAPI-vet.git
   ```

Create a virtual environment

```
python -m venv venv
venv\Scripts\Activate.ps1
```

Install dependencies:

```
pip install -r requirements.txt
```

Configure environment variables:

Create a .env file in the project root directory and add the following:

```
SECRET_KEY=your_secret_key_here
```

Run the RestAPI application:

Set environment in terminal:

```
 $env:MONGODB_URL="your_mongodb_url"
```

```
uvicorn main:app
```

Vets exclusively manage their individual animal patients and treatments. Only the vet can delete their own profile.

Access the API documentation at http://localhost:8000/docs in your web browser.

### API Documentation

API documentation is automatically generated using Swagger UI. You can access it at http://localhost:8000/docs after running the application.

## Author:

Kristina Holovka
