import subprocess
from paths import TEST_FILE, ALLURE_RESULTS_DIR


def main():
    subprocess.run([
        "pytest",
        TEST_FILE,
        f"--alluredir={ALLURE_RESULTS_DIR}"
    ])


if __name__ == "__main__":
    main()
