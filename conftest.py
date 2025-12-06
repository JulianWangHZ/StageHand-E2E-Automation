import asyncio
import os
import random
import shutil
import tempfile
from typing import Generator

import pytest
from dotenv import load_dotenv
from stagehand import Stagehand, StagehandConfig

from config.devices import get_device_class

# Load environment variables from .env file
load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--device",
        action="store",
        default="desktop",
        choices=["mobile", "ipad", "tablet", "desktop"],
        help="Device type to use for tests (mobile, ipad, tablet, desktop). 'tablet' is an alias for 'ipad'",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )
    parser.addoption(
        "--stagehand-model",
        action="store",
        default="gpt-5-nano",
        help="Stagehand model name to use",
    )


@pytest.fixture(scope="function")
async def stagehand_on_demand(request) -> Generator[Stagehand, None, None]:
    device_type = request.config.getoption("--device", default="desktop")
    device_instance = get_device_class(device_type)
    
    # Generate random port to avoid conflicts
    debug_port = 9222 + random.randint(0, 1000)
    user_data_dir = tempfile.mkdtemp(
        prefix=f"stagehand_test_{random.randint(1000, 9999)}_"
    )
    
    # Handle parallel execution with pytest-xdist
    worker_id = os.environ.get('PYTEST_XDIST_WORKER', 'main')
    if worker_id != 'main':
        # Add longer delay for parallel execution
        delay = random.uniform(0.5, 2.0)
        print(f"Worker {worker_id}: Delaying {delay:.2f} seconds to avoid resource conflicts")
        await asyncio.sleep(delay)
    else:
        await asyncio.sleep(random.uniform(0.1, 0.3))
    
    # Stagehand configuration
    config = StagehandConfig(
        env="LOCAL",
        model_name=request.config.getoption("--stagehand-model", default="gpt-5-nano"),
        model_api_key=os.getenv('OPENAI_API_KEY'),
        verbose=1,
        local_browser_launch_options={
            "headless": request.config.getoption("--headless", default=False),
            "user_data_dir": user_data_dir,
            "viewport": {
                "width": device_instance.width,
                "height": device_instance.height,
            },
            "args": [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                f"--remote-debugging-port={debug_port}",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-extensions",
                "--disable-plugins",
                "--disable-default-apps",
                "--disable-sync",
                "--disable-translate",
                "--disable-component-extensions-with-background-pages",
                "--memory-pressure-off",
                "--max_old_space_size=4096",
                "--disable-background-networking",
                "--disable-background-timer-throttling",
                "--disable-client-side-phishing-detection",
                "--disable-default-apps",
                "--disable-hang-monitor",
                "--disable-prompt-on-repost",
                "--disable-domain-reliability",
                "--disable-features=TranslateUI",
                "--disable-ipc-flooding-protection",
                "--disable-blink-features=AutomationControlled"
            ] + (["--headless"] if request.config.getoption("--headless", default=False) else [])
        }
    )
    
    stagehand = Stagehand(config)
    
    try:
        await stagehand.init()
        yield stagehand
    except Exception as e:
        print(f"❌ Stagehand initialization failed: {e}")
        raise
    finally:
        try:
            await stagehand.close()
        except Exception as e:
            print(f"Error closing Stagehand: {e}")
        finally:
            try:
                shutil.rmtree(user_data_dir, ignore_errors=True)
            except OSError:
                pass
            await asyncio.sleep(1)

