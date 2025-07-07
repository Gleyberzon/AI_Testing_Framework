import subprocess
from paths import BROWSERUSE_TESTS_PATH, ALLURE_RESULTS_DIR, ALUMNIUM_TESTS_PATH

# !!! Read README.txt before starting !!!

def main():
    subprocess.run([
        "pytest",
        BROWSERUSE_TESTS_PATH, ### Add tasks to file Task/browseruse_tasks.csv for BrowserUse testing.
        # ALUMNIUM_TESTS_PATH, ### Develop your own tests with Alumnium
        f"--alluredir={ALLURE_RESULTS_DIR}"
    ])


if __name__ == "__main__":
    main()
