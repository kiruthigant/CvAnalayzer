# CV Analyzer

CV Analyzer is an intelligent tool that helps you analyze your resume and discover job roles that best match your skills and experience. Simply upload your CV, and the system extracts relevant information to provide actionable career insights.

## Features

- **Resume Parsing**: Extracts text from PDF and DOCX files.
- **AI-Powered Analysis**: Utilizes OpenAI to analyze the extracted CV information.
- **Role Recommendations**: Suggests potential job roles you can apply for based on your profile.
- **Modern UI**: Clean and responsive frontend built with React and Tailwind CSS.

## Tech Stack

### Frontend
- **React 18** (with Vite)
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **Axios** for API requests

### Backend
- **FastAPI** for high-performance API endpoints
- **SQLAlchemy** for database operations
- **OpenAI API** for intelligent CV analysis
- **pdfplumber & python-docx** for document processing
- **Uvicorn** for serving the backend

## Prerequisites

Before running the project, make sure you have the following installed:
- Node.js (v18 or higher)
- Python (v3.9 or higher)
- An OpenAI API key

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd CvAnalayzer
```

### 2. Backend Setup

Navigate to the backend directory and set up the Python environment:

```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory with your environment variables (e.g., OpenAI API Key, Database URL):

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=your_database_url_here
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```
*(Note: Ensure the entry point matches your actual FastAPI app structure)*

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

## Usage

1. Open your browser and navigate to the frontend URL (usually `http://localhost:5173`).
2. Upload your CV (PDF or DOCX format).
3. Wait for the analysis to complete.
4. Review the extracted information and the recommended job roles tailored to your profile.
