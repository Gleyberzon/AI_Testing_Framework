import os

# Root is the current folder
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

BROWSERUSE_TESTS_PATH = os.path.join(PROJECT_ROOT, "BrowserUseTests", "test_BrowserUse.py")
ALUMNIUM_TESTS_PATH = os.path.join(PROJECT_ROOT, "AlumniumTests", "test_alumnium.py")
CSV_FILE_PATH = os.path.join(PROJECT_ROOT, "Tasks", "browseruse_tasks.csv")
ALLURE_RESULTS_DIR = os.path.join(PROJECT_ROOT, "allure-results")
ENV_FILE = os.path.join(PROJECT_ROOT, ".env")
