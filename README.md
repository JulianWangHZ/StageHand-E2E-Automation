# Stagehand E2E Automation Framework

A comprehensive end-to-end testing framework built with [Stagehand](https://github.com/browserbase/stagehand-python) and pytest for automated browser testing using natural language instructions.

## Overview

This framework enables reliable browser automation by combining the power of AI-driven natural language commands with traditional code-based testing. It's specifically configured for testing the TransGlobal website (https://www.transglobalus.com/) with support for multiple device types, parallel execution, and automatic retry mechanisms.

> ⚠️ **IMPORTANT BROWSER LIMITATION**: Stagehand **ONLY** supports Chromium/Chrome browsers. **Firefox and Safari are NOT supported** and will not work with this framework.

## Features

- **Natural Language Testing**: Write tests using plain English instructions
- **Multi-Device Support**: Test on mobile, iPad, and desktop viewports
- **Parallel Execution**: Run tests in parallel using pytest-xdist
- **Automatic Retry**: Failed tests automatically retry with configurable attempts
- **Flexible Tagging**: Organize tests using custom markers (tags)
- **Production-Ready**: Designed for reliable CI/CD integration

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Best Practices](#best-practices)
- [Coding Standards](#coding-standards)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (Python 3.10+ recommended)
- **pip** or **uv** (package manager)
- **OpenAI API Key** (required for Stagehand)
- **Git** (for cloning the repository)

### System Requirements

- macOS, Linux, or Windows
- At least 2GB of free disk space
- Internet connection for API calls and browser downloads

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd StageHand-E2E-Automation
```

### Step 2: Create a Virtual Environment

Using `venv` (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Or using `uv` (faster alternative):

```bash
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or with `uv`:

```bash
uv pip install -r requirements.txt
```

### Step 4: Install Playwright Browser

> ⚠️ **CRITICAL**: Stagehand **ONLY** supports Chromium/Chrome browsers. **Firefox and Safari are NOT supported**. Do not attempt to install or use other browsers.

Install Chromium browser for local execution:

```bash
python -m playwright install chromium
```

This will download and install the Chromium browser required by Stagehand for browser automation.

### Step 5: Configure Environment Variables

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_actual_openai_api_key_here
```

**Important**: Never commit the `.env` file to version control. It's already included in `.gitignore`.

### Step 6: Verify Installation

Run a simple test to verify everything is set up correctly:

```bash
pytest tests/pages/homepage/test_homepage.py::test_homepage_loads -v
```

If the test runs successfully, you're ready to go! 🎉

## Configuration

### Device Types

The framework supports three device configurations:

- **mobile**: 430x932 (iPhone 15 Pro Max size)
- **ipad**: 1024x1366 (iPad Pro 12.9" size)
- **desktop**: 1920x1080 (default)

### Browser Support

> ⚠️ **BROWSER COMPATIBILITY WARNING**
> 
> **Stagehand ONLY supports Chromium-based browsers:**
> - ✅ Chrome
> - ✅ Chromium
> - ✅ Microsoft Edge (Chromium-based)
> 
> **NOT supported:**
> - ❌ Firefox
> - ❌ Safari
> - ❌ Any other non-Chromium browsers
> 
> The framework uses Playwright's Chromium browser for all test executions. Attempting to use unsupported browsers will result in errors.

### Pytest Configuration

The `pytest.ini` file contains all test configuration:

- **Test Discovery**: Automatically finds tests in the `tests/` directory
- **Markers**: Custom tags for organizing tests (configured in `pytest.ini`)
- **Retry Settings**: Default 2 retries with 1 second delay
- **Logging**: Configured for detailed test output

## Running Tests

### Basic Test Execution

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/pages/homepage/test_homepage.py
```

Run specific test function:

```bash
pytest tests/pages/homepage/test_homepage.py::test_homepage_loads
```

### Using Device Options

Run tests on mobile device:

```bash
pytest --device=mobile
```

Run tests on iPad:

```bash
pytest --device=ipad
```

Run tests on desktop (default):

```bash
pytest --device=desktop
```

### Using Tags (Markers)

Run only smoke tests:

```bash
pytest -m smoke
```

Run critical tests:

```bash
pytest -m critical
```

Run homepage tests:

```bash
pytest -m homepage
```

Combine multiple tags (OR logic):

```bash
pytest -m "smoke or critical"
```

Combine multiple tags (AND logic):

```bash
pytest -m "smoke and homepage"
```

Exclude specific tags:

```bash
pytest -m "not regression"
```

### Headless Mode

Run tests in headless mode (no browser window):

```bash
pytest --headless
```

### Parallel Execution

Run tests in parallel (faster execution):

```bash
pytest -n auto  # Automatically detect CPU cores
pytest -n 4     # Use 4 workers
```

### Combining Options

Run smoke tests on mobile in headless mode with parallel execution:

```bash
pytest -m smoke --device=mobile --headless -n auto
```

### Model Selection

Use a different Stagehand model:

```bash
pytest --stagehand-model=gpt-4o
```

### Verbose Output

Get detailed test output:

```bash
pytest -v  # Verbose
pytest -vv  # More verbose
pytest -s   # Show print statements
```

### Retry Configuration

The default retry configuration is set in `pytest.ini` (2 retries with 1 second delay). You can override it:

```bash
pytest --reruns=3 --reruns-delay=2
```

## Best Practices

### 1. Use Descriptive Test Names

```python
# Good
async def test_homepage_services_section_displays_correctly(stagehand_on_demand):
    pass

# Bad
async def test1(stagehand_on_demand):
    pass
```

### 2. Add Appropriate Markers

Always tag your tests appropriately:

```python
@pytest.mark.homepage
@pytest.mark.smoke
async def test_homepage_loads(stagehand_on_demand):
    pass
```

### 3. Use Specific Natural Language Instructions

```python
# Good - specific
await page.act("click the 'Get Started' button in the hero section")

# Bad - vague
await page.act("click button")
```

### 4. Handle Errors Gracefully

```python
try:
    await page.act("click the submit button")
except Exception as e:
    # Log or handle the error appropriately
    print(f"Action failed: {e}")
    raise
```

### 5. Cache Actions When Possible

Use `observe` to preview actions and cache them:

```python
# Preview the action
action = await page.observe("click the navigation menu")

# Execute without additional LLM call
await page.act(action[0])
```

### 6. Use Structured Data Extraction

For complex data, use Pydantic schemas:

```python
from pydantic import BaseModel

class ServiceInfo(BaseModel):
    title: str
    description: str
    link: str

services = await page.extract("all services", schema=ServiceInfo)
```

### 7. Keep Tests Independent

Each test should be able to run independently:

```python
# Good - each test navigates to the page
async def test_a(stagehand_on_demand):
    await stagehand_on_demand.page.goto("https://www.transglobalus.com/")
    # test code

async def test_b(stagehand_on_demand):
    await stagehand_on_demand.page.goto("https://www.transglobalus.com/")
    # test code
```

### 8. Use BaseActions for Common Operations

Always use `BaseActions` for standard Playwright operations to maintain consistency and reusability:

```python
from tests.pages.base.base_action import BaseActions

base_actions = BaseActions(page)
await base_actions.open_url("https://www.transglobalus.com/")
await base_actions.wait_for_page_loaded()
is_visible = await base_actions.verify_element_visible('selector')
```

### 9. Verify Page Content, Not Just URLs

Always verify that page content has actually loaded, not just that the URL changed:

```python
# Good - verifies content is loaded
await base_actions.wait_for_page_loaded()
current_url = page.url
assert "contact" in current_url.lower()
body_text = await base_actions.get_element_text("body")
assert len(body_text.strip()) > 0, "Page appears to be blank"

# Bad - only checks URL
current_url = page.url
assert "contact" in current_url.lower()
```

## Coding Standards

This project follows Python best practices and coding principles. For detailed coding rules, see [`.cursor/rules/stagehand_coding_rules.mdc`](.cursor/rules/stagehand_coding_rules.mdc).

### PEP 8 Style Guide

- **Naming Conventions**:
  - Modules: `snake_case` (e.g., `test_header.py`)
  - Classes: `PascalCase` (e.g., `BaseActions`, `Device`)
  - Functions/Methods: `snake_case` (e.g., `navigate_homepage`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_TIMEOUT`)
  - Private methods: Prefix with `_` (e.g., `_resolve_locator`)

- **Code Formatting**:
  - Maximum 100 characters per line (soft limit)
  - Use 4 spaces for indentation (never tabs)
  - 2 blank lines between top-level definitions
  - 1 blank line between methods
  - Group imports: standard library, third-party, local

- **Import Organization**:
```python
# Standard library
import asyncio
from typing import Union

# Third-party
import pytest
from playwright.async_api import Page
from stagehand import Stagehand

# Local
from tests.pages.base.base_action import BaseActions
from config.devices import get_device_class
```

### SOLID Principles

- **Single Responsibility**: Each class/function should have one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable for their base types
- **Interface Segregation**: Keep interfaces focused and minimal
- **Dependency Inversion**: Depend on abstractions, not concretions

### DRY Principle

- Extract common functionality into reusable functions/classes
- Use `BaseActions` for common Playwright operations
- Create helper functions for repeated patterns
- Use fixtures for shared test setup

### Pytest-BDD Structure

#### Feature Files
- Location: `features/{page_name}/{feature_name}.feature`
- Use Gherkin syntax (Given-When-Then)
- Tag scenarios appropriately (e.g., `@homepage`, `@header_visibility`)

#### Test Files
- Location: `tests/pages/{page_name}/test_{feature_name}.py`
- Use `scenarios()` function at the top to load feature files
- Write all steps for each scenario together
- **Do NOT** prefix step definition functions with `given_`, `when_`, `then_`

#### Example Structure:
```python
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from stagehand import Stagehand
from tests.pages.base.base_action import BaseActions

scenarios('../../../features/homepage/header.feature')

@given("I navigate to the TransGlobal homepage")
async def navigate_homepage_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.open_url("https://www.transglobalus.com/")
    await base_actions.wait_for_page_loaded()

@when("I look at the header")
async def look_at_header_visibility(stagehand_on_demand: Stagehand):
    await stagehand_on_demand.page.wait_for_timeout(500)

@then("the TransGlobal logo should be visible")
async def logo_visible_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    is_visible = await base_actions.verify_element_visible('a[href*="transglobalus.com"]')
    assert is_visible
```

### Stagehand Usage Guidelines

- **Use BaseActions** for standard Playwright operations (click, wait, verify)
- **Use `page.act()`** for natural language actions that require AI interpretation
- **Use `page.observe()`** only when necessary (preview actions before execution)
- **Use `page.extract()`** only when structured data extraction is needed
- Be specific in natural language instructions

### Test Organization

- **File Structure**: Organize tests by page/feature (e.g., `tests/pages/homepage/test_header.py`)
- **Naming**: Test files use `test_{feature_name}.py`, feature files use `{feature_name}.feature`
- **Tags**: Use scenario-specific tags (e.g., `@header_visibility`, `@header_click_contact`) and page-level tags (e.g., `@homepage`)
- **Independence**: Each test should be able to run independently

### Code Quality Standards

- **Functions**: Keep functions small and focused (max 50 lines, prefer shorter)
- **Variables**: Use descriptive names, avoid abbreviations
- **Type Hints**: Use type hints for function parameters and return values
- **Comments**: Comment "why", not "what"
- **Constants**: Define constants at module level, avoid magic numbers

### Common Patterns

#### Navigation Pattern
```python
@given("I navigate to the TransGlobal homepage")
async def navigate_homepage(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.open_url("https://www.transglobalus.com/")
    await base_actions.wait_for_page_loaded()
```

#### Click and Navigate Pattern
```python
@when("I click the menu item")
async def click_menu_item(stagehand_on_demand: Stagehand, menu_item: str):
    page = stagehand_on_demand.page
    await page.act(f'click the "{menu_item}" in the header')
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(2000)  # Wait for content to load

@then("I should be navigated to the page")
async def verify_navigation(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.wait_for_page_loaded()
    current_url = page.url
    assert "expected-path" in current_url.lower()
    # Verify page content is loaded
    body_text = await base_actions.get_element_text("body")
    assert len(body_text.strip()) > 0, "Page appears to be blank"
```

### Anti-Patterns to Avoid

❌ **Don't Do This**:
```python
# Magic numbers
await page.wait_for_timeout(2000)

# Generic names
def test1(stagehand):
    pass

# Code duplication
await page.locator('selector').wait_for(state="visible")
# Repeated in multiple places

# No page content verification
current_url = page.url
assert "contact" in current_url.lower()

# Prefixing with given/when/then
async def given_navigate_homepage(...):
    pass
```

✅ **Do This Instead**:
```python
# Named constant or variable
PAGE_LOAD_DELAY = 2000
await page.wait_for_timeout(PAGE_LOAD_DELAY)

# Descriptive names
async def test_header_logo_visibility(stagehand):
    pass

# Use BaseActions
base_actions = BaseActions(page)
is_visible = await base_actions.verify_element_visible('selector')

# Verify page content
base_actions = BaseActions(page)
await base_actions.wait_for_page_loaded()
body_text = await base_actions.get_element_text("body")
assert len(body_text.strip()) > 0, "Page appears to be blank"

# No prefix
async def navigate_homepage(...):
    pass
```

For complete coding rules and detailed guidelines, refer to [`.cursor/rules/stagehand_coding_rules.mdc`](.cursor/rules/stagehand_coding_rules.mdc).

## Troubleshooting

### Common Issues

#### 1. "OPENAI_API_KEY not found"

**Problem**: Missing or incorrect API key in `.env` file.

**Solution**:
- Verify `.env` file exists in the project root
- Check that `OPENAI_API_KEY` is set correctly
- Ensure `.env` file is not committed to git

#### 2. "Browser not found" or "Chromium not installed"

**Problem**: Playwright browser not installed.

**Solution**:
```bash
python -m playwright install chromium
```

> ⚠️ **WARNING**: Only Chromium browser is supported. **Do NOT** attempt to install Firefox or Safari browsers as Stagehand does not support them.

#### 3. Port conflicts in parallel execution

**Problem**: Multiple tests trying to use the same port.

**Solution**: The framework automatically handles this with random ports. If issues persist, reduce the number of parallel workers:

```bash
pytest -n 2  # Instead of -n auto
```

#### 4. Tests timing out

**Problem**: Tests taking too long or hanging.

**Solution**:
- Check your internet connection
- Verify the target website is accessible
- Increase timeout in test code if needed
- Check OpenAI API rate limits

#### 5. "Module not found" errors

**Problem**: Dependencies not installed.

**Solution**:
```bash
pip install -r requirements.txt
```

#### 6. Headless mode issues

**Problem**: Tests fail in headless mode but pass in headed mode.

**Solution**:
- Some websites behave differently in headless mode
- Try running without `--headless` flag first
- Check if the website blocks headless browsers

#### 7. Browser compatibility issues

**Problem**: Attempting to use Firefox or Safari, or getting errors about unsupported browsers.

> ⚠️ **IMPORTANT**: Stagehand **ONLY** supports Chromium/Chrome browsers. Firefox and Safari are **NOT supported**.

**Solution**:
- ✅ Ensure you have Chromium installed via `python -m playwright install chromium`
- ❌ **Do NOT** configure the framework to use Firefox or Safari
- ❌ **Do NOT** attempt to install Firefox or Safari browsers
- If you see browser compatibility errors, verify that Chromium is properly installed

### Getting Help

1. Check the [Stagehand documentation](https://github.com/browserbase/stagehand-python)
2. Review pytest logs with `-v` or `-vv` flags
3. Run tests with `-s` flag to see print statements
4. Check browser console logs in non-headless mode

### Debug Mode

Run tests with maximum verbosity:

```bash
pytest -vvv -s --tb=long
```

This will show:
- Very verbose output
- Print statements
- Full traceback for failures

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Resources

- [Stagehand Python Documentation](https://github.com/browserbase/stagehand-python)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/)
- [Pytest-rerunfailures Documentation](https://github.com/pytest-dev/pytest-rerunfailures)

---

**Happy Testing! 🚀**

