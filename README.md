# Chemical Equipment Management System

This project is a web application for managing chemical equipment. It consists of a Django backend and a React frontend.

## Local Development Setup

### Prerequisites

- Python 3.x
- Node.js and npm

### Backend

1.  **Navigate to the root directory.**
2.  **Run the backend setup script:**
    ```bash
    ./run_backend.sh
    ```
    This script will create a virtual environment, install the required packages, run database migrations, and start the development server at `http://127.0.0.1:8000`.

### Frontend

1.  **Open a new terminal.**
2.  **Navigate to the root directory.**
3.  **Run the frontend setup script:**
    ```bash
    ./run_frontend.sh
    ```
    This script will install the required packages and start the development server at `http://localhost:3000`.

### Environment Variables

Before running the application, you need to create a `.env` file in the `backend` directory and add the necessary environment variables. You can use the `.env.example` file as a template.