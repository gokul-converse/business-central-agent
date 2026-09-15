# Business Central Agent

An AI agent built using Microsoft Agent Framework and Business Central APIs.

## Features

- Search Business Central customers
- Create customers
- Update customer details
- Delete customers
- Business Central OAuth token handling
- MAF tool integration
- FastAPI backend

## Tech Stack

- Python
- FastAPI
- Microsoft Agent Framework
- Azure AI Foundry
- Business Central REST API
- Microsoft Entra ID
- Pydantic
- HTTPX

## Project Structure

```text
app/
├── agents/
├── api/
├── auth/
├── business_central/
├── models/
├── services/
└── tools/


Setup
1. Clone the repository
git clone <your-repository-url>
cd business-central-agent
2. Create a virtual environment
python -m venv venv
3. Activate the environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Configure environment variables

Create a .env file using .env.example.

6. Run the application
uvicorn app.main:app --reload