# Flask RAG Application

## Overview
This is a Flask-based application for managing documents and answering questions using Retrieval-Augmented Generation (RAG).

## Features
- User authentication (register, login, logout).
- Document upload and retrieval.
- Question-answering system.

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
2. Create a virtual environment:
   ```bash
   python -m venv ragenv
   source ragenv/bin/activate

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Database Configuration
1. Update the database URI in app/utils.py:
   ```bash
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<username>:<password>@localhost/<database-name>'
2. Create the database in PostgreSQL:
   ```bash
   createdb flask_rag_db
3. Initialize the database:
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
## Running the application
1. Start the Flask development server:
   ```bash
   python run.py
## Docker Setup 
1. Build the Docker image:
   ```bash
   docker-compose build
2. Run the application using Docker:
   ```bash
   docker-compose up
## API Documentation
### Authentication
- Register a User:

  - Endpoint: POST /register
  - Request Body:
   ```bash
  {
  "username": "testuser",
  "password": "testpass",
  "role": "user"
   }
  ```  
  - Response:
  ```bash
  - {
  "message": "User Registered Successfully"
   } 
  ```
- Login:

  - Endpoint: POST /login
  - Request Body:
  ```bash
  {
  "username": "testuser",
  "password": "testpass"
   } 
  ```
  - Response
  ```bash
  {
  "access_token": "<JWT_TOKEN>"
   }
  ```
- Logout:

   - Endpoint: POST /logout
   - Headers:
  ```bash
   Authorization: Bearer <JWT_TOKEN>
  ```
   - Response:
   ```bash
   {
      "message": "User logged out successfully"
   }
   ```
Document Management
- Upload a Document:
  - Endpoint: POST /upload
  - Headers:
  ```bash 
   Authorization: Bearer <JWT_TOKEN>
   ```
  - Request Body (form-data):
  ```bash
  file: <file>
  ```
  - Response:
  ```bash
   {
  "message": "File uploaded successfully",
  "document_id": 1
   }
  ```
- Get Document Metadata:

  - Endpoint: GET /document/<int:document_id>
  - Headers:
  ```bash 
   Authorization: Bearer <JWT_TOKEN>
  ```
  - Response:
   ```bash
   {
     "document_id": 1,
     "filename": "testfile.txt",
     "file_url": "http://example.com/testfile.txt",
     "uploaded_at": "2023-10-01T12:34:56"
   }
  ```
Testing

To run the unit tests:

```bash
   python -m unittest discover tests
```
Deployment
   - Local Deployment: Use run.py to start the Flask development server.
   - Docker Deployment: Use docker-compose up to deploy the application in a containerized environment.