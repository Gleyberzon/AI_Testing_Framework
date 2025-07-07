# pip install allure-pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import csv
import pytest
import allure  # Import the allure library
from browser_use import Agent
from dotenv import load_dotenv
from browser_use.llm import ChatGoogle
from selenium.webdriver import Chrome
from alumnium import Alumni
from paths import CSV_FILE_PATH


load_dotenv()

# --- Pytest Fixtures ---


@pytest.fixture(scope="function")
def alumni_session():
    """ Provides a Selenium Chrome driver and an Alumni object for each test function """
    driver = None
    al = None
    try:
        driver = Chrome()
        driver.get("https://todomvc.com/examples/vue/dist/#/")
        al = Alumni(driver)
        yield al
    finally:
        if driver:
            driver.quit()


@pytest.fixture(scope="module")
def gemini_llm():
    """Fixture to initialize the Gemini LLM, skipping tests if API key is missing or fails."""
    try:
        llm = ChatGoogle(model='gemini-2.0-flash-exp')
        return llm
    except Exception as e:
        # Allure will show this as a skipped test with the reason
        pytest.skip(f"Failed to initialize or connect to Gemini LLM: {e}")
        return None  # Should not be reached due to skip


# --- Helper Function to Read Test Data ---


def load_test_data_from_csv(file_path):
    """Reads test data from a CSV file."""
    test_data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip header row

            if header != ["Test Name", "Test Task", "Expected Substring"]:
                # Use pytest.fail here as this prevents any tests from running with bad data
                pytest.fail(
                    f"CSV header mismatch. Expected ['Test Name', 'Test Task', 'Expected Substring'], got {header}")

            for row in reader:
                if len(row) == 3:
                    test_name, test_task, expected_substring = row
                    test_data.append(
                        (test_name, test_task, expected_substring))
                else:
                    # Use print here, as it's just a warning, not failure
                    print(f"Warning: Skipping malformed row in CSV: {row}")

    except FileNotFoundError:
        pytest.fail(f"Test data CSV file not found: {file_path}")
    except Exception as e:
        pytest.fail(f"An error occurred while reading CSV: {e}")

    if not test_data:
        pytest.fail(f"No test data found in CSV file: {file_path}")

    return test_data


# --- Async Helper Function to Run Agent ---

async def run_task(task_string: str, llm_instance):
    """Runs the browser agent for a given task and returns the final result."""
    agent = Agent(
        task=task_string,
        llm=llm_instance,
        verbose=True,
        timeout=120
    )
    # We'll wrap the call to this function in an Allure step in the test itself
    try:
        logs = await agent.run()
        final_result = logs.final_result()
        return final_result
    except Exception as e:
        # Log the exception and return an error indicator
        print(f"An error occurred during task '{task_string}': {e}")
        # Re-raise the exception or return a specific error value if needed for assertion
        # For this example, let's return a string indicating failure due to execution error
        return f"Execution Error: {e}"


# --- Pytest Parametrized Test Function with Allure ---

# Load the data once for parametrization
test_cases = load_test_data_from_csv(CSV_FILE_PATH)


@pytest.mark.asyncio  # Indicates that this test function is an async coroutine
@allure.feature("Browser Automation Agent")  # Adds a Feature to the report
@allure.story("Execute Task from CSV")      # Adds a Story to the report
@pytest.mark.parametrize(
    "test_name, test_task, expected_substring",
    test_cases,
    # Use the 'test_name' from the CSV as the ID for Pytest/Allure reporting
    ids=[case[0] for case in test_cases]
)
async def test_browser_task_from_csv(test_name: str, test_task: str, expected_substring: str, gemini_llm):
    """
    Runs browser tasks defined in the CSV file and asserts the expected substring
    is present in the final result.
    """
    # Use the test_name from CSV as the title in the Allure report
    allure.dynamic.title(test_name)
    # Add parameters explicitly (parametrize often does this, but explicit is clearer)
    allure.dynamic.parameter("Task Description", test_task)
    allure.dynamic.parameter("Expected Substring", expected_substring)

    assert gemini_llm is not None  # Should be true unless the fixture caused a skip

    # Wrap the core execution logic in an Allure step
    with allure.step(f"Execute browser task: '{test_task}'"):
        final_result = await run_task(test_task, gemini_llm)

    # Assert that the expected substring is present in the final result
    # The assertion message is still useful in console output and detailed Allure logs
    assert expected_substring in str(final_result), \
        f"Test '{test_name}' failed.\n" \
        f"Task: '{test_task}'\n" \
        f"Expected substring: '{expected_substring}'\n" \
        f"Actual final result: '{final_result}'"
