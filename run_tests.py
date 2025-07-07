import subprocess
from paths import BROWSERUSE_TESTS_PATH, ALLURE_RESULTS_DIR

### Add tasks to file Task/browseruse_tasks.csv
def main():
    subprocess.run([
        "pytest",
        BROWSERUSE_TESTS_PATH,
        f"--alluredir={ALLURE_RESULTS_DIR}"
    ])


if __name__ == "__main__":
    main()
