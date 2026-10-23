CivicSense AI — fixed Windows setup

Use `python`, not `py`, because the Python launcher is unavailable on your machine.

1. Check:
   python --version
   python -m pip --version

2. Create environment:
   python -m venv .venv

3. Activate:
   .\.venv\Scripts\Activate.ps1

If activation is blocked:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1

4. Install:
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt

5. Prepare data and train:
   python scripts/generate_demo_dataset.py
   python scripts/train_models.py

6. Terminal 1:
   python -m uvicorn backend.main:app --reload --port 8000

7. Terminal 2 (project folder; activate .venv):
   python -m streamlit run app/Home.py

Open the Streamlit URL printed in terminal. API docs: http://127.0.0.1:8000/docs
If `python --version` is not recognized, install Python from python.org and tick “Add python.exe to PATH”.
