### Prerequisites
- Python 3.9+
- Node.js 18+
- npm
- Git

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

### Frontend Setup
cd frontend
npm install
npm start

### Usage

Open the dashboard in your browser.
View incident cards and description.
Click on a card to view detailed incident information.
