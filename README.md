# To do App
 
 This is a FastAPI-based To do list API that allows users to create, retrieve, update, and delete tasks. It uses MongoDB as the backend database and integrates user authentication to restrict access to authorized users.

## How to Run the Project
### Prerequisites
1. Python 3.9 or later
2. MongoDB installed and running
3. pip for Python package management

## Installation
### Clone the repository:

    git clone https://github.com/AishV05/To-do-App.git
    cd To-do-App
    cd backend
    
### Create a virtual environment:

    python -m venv venv
    source venv/bin/activate  
    # On Windows:venv\Scripts\activate
### Install dependencies:

    pip install -r requirements.txt

### Set up your .env file:

    DATABASE_URL=mongodb://localhost:27017
    SECRET_KEY=your_secret_key
### Run the application:

    uvicorn main:app --reload
