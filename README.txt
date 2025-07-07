# 🧪 AI Test Framework

This project automates browser tasks using AI agents and is powered by Playwright, Pytest, and Allure reporting.

✅ Getting Started

Follow these steps to set up and run the project locally:

---

### 1. Create a virtual environment in the project root:

python -m venv venv

### 2. Activate virtual environment

venv/Scripts/activate

### 3. Install all nesessary modules

pip install -r requirements.txt

### 4. Install playwright

playwright install

### 5. Execute tests

python run_tests.py

### 6. Open allure report

allure serve allure-results

If allure not installed - execute once next steps:
 - Install java JDK if not installed (Validate installation with command "java -version")
 - Open powershell as admin and execute:

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
scoop install allure




