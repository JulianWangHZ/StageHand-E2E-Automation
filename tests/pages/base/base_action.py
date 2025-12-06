import asyncio
from typing import Union

from playwright.async_api import Locator, Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


class BaseActions:
    def __init__(self, page: Page, default_timeout: int = 30):
        self.page = page
        self.default_timeout = default_timeout

    async def wait_for_page_loaded(self):
        await self.page.wait_for_load_state("domcontentloaded")
        await self.page.wait_for_load_state("load")

    def _resolve_locator(self, locator: Union[Locator, str]) -> Locator:
        """
        Resolve locator to Playwright Locator object.

        **Preferred**: Pass Playwright Locator objects directly.
        String format (CSS selector) is supported for backward compatibility only.

        Args:
            locator: Playwright Locator object (preferred) or CSS selector string

        Returns:
            Playwright Locator object
        """
        if isinstance(locator, Locator):
            return locator
        if isinstance(locator, str):
            return self.page.locator(locator)
        raise TypeError(
            f"Unsupported locator type: {type(locator)}. Expected Locator or str."
        )

    async def open_url(self, url: str):
        """
        Opens the specified URL in the browser.

        Args:
            url: Full URL to open
        """
        await self.page.goto(
            url, wait_until="domcontentloaded", timeout=self.default_timeout * 1000
        )

    async def find_element(self, locator: Union[Locator, str]):
        resolved_locator = self._resolve_locator(locator)
        await resolved_locator.wait_for(
            state="attached", timeout=self.default_timeout * 1000
        )
        return resolved_locator

    async def is_element_visible(self, locator: Union[Locator, str]):
        try:
            resolved_locator = self._resolve_locator(locator)
            await resolved_locator.wait_for(
                state="visible", timeout=self.default_timeout * 1000
            )
            return True
        except PlaywrightTimeoutError:
            return False

    async def click_element(self, locator: Union[Locator, str]):
        """
        Note: Playwright's click() automatically waits for element to be actionable:
        - Attached to DOM
        - Visible
        - Stable (not animating)
        - Receives events (not covered)
        - Enabled
        """
        resolved_locator = self._resolve_locator(locator)
        await resolved_locator.click(timeout=self.default_timeout * 1000)

    async def click_if_exists(self, locator: Union[Locator, str]):
        if await self.is_element_visible(locator):
            await self.click_element(locator)
            return True
        return False

    async def clear_element_text(self, locator: Union[Locator, str]):
        resolved_locator = self._resolve_locator(locator)
        current_value = await resolved_locator.input_value()
        if not current_value or current_value.strip() == "":
            return True

        await resolved_locator.clear()
        max_attempts = 5
        attempts = 0
        while attempts < max_attempts:
            cleared_value = await resolved_locator.input_value()
            if not cleared_value or cleared_value.strip() == "":
                return True

            await resolved_locator.clear()
            attempts += 1
            await self.page.wait_for_timeout(200)

        if attempts == max_attempts:
            final_value = await resolved_locator.input_value()
            print(f"警告: 無法清空欄位，當前值: {final_value}")
            return False

        return True

    async def send_keys_to_element(self, locator: Union[Locator, str], text: str):
        """
        Note: Playwright's input_value(), clear(), and fill() automatically wait for elements to be:
        """
        resolved_locator = self._resolve_locator(locator)

        current_value = await resolved_locator.input_value()

        if current_value:
            await resolved_locator.clear()

            max_attempts = 5
            attempts = 0
            while attempts < max_attempts:
                cleared_value = await resolved_locator.input_value()
                if not cleared_value or cleared_value.strip() == "":
                    break

                await resolved_locator.clear()
                attempts += 1

            if attempts == max_attempts:
                final_value = await resolved_locator.input_value()
                print(f"Warning: Unable to clear field, current value: {final_value}")

        text = str(text)
        await resolved_locator.fill(text)

    async def get_element_text(self, locator: Union[Locator, str]):
        """
        Note: Playwright's inner_text() automatically waits for element to be visible.
        """
        resolved_locator = self._resolve_locator(locator)
        return await resolved_locator.inner_text()

    async def wait_for_element_visible(
        self, locator: Union[Locator, str], timeout=None
    ):
        try:
            resolved_locator = self._resolve_locator(locator)
            timeout_ms = (timeout * 1000) if timeout else (self.default_timeout * 1000)
            await resolved_locator.wait_for(state="visible", timeout=timeout_ms)
        except PlaywrightTimeoutError:
            raise PlaywrightTimeoutError(f"Element not found or not visible: {locator}")

    async def wait_for_element_clickable(
        self, locator: Union[Locator, str], timeout=10
    ):
        try:
            resolved_locator = self._resolve_locator(locator)
            await resolved_locator.wait_for(state="visible", timeout=timeout * 1000)
            is_disabled = await resolved_locator.get_attribute("disabled")
            if is_disabled is not None:
                raise PlaywrightTimeoutError(f"Element is disabled: {locator}")
            return True
        except PlaywrightTimeoutError as e:
            raise PlaywrightTimeoutError(
                f"Element not clickable within {timeout} seconds: {locator}. Error: {e}"
            )

    async def wait_for_element_present(self, locator: Union[Locator, str], timeout=3):
        resolved_locator = self._resolve_locator(locator)
        await resolved_locator.wait_for(state="attached", timeout=timeout * 1000)
        return True

    async def wait_for_flash_present_then_disappear(
        self,
        locator: Union[Locator, str],
        appear_timeout: int = 3,
        disappear_timeout: int = 5,
    ):
        await self.wait_for_element_present(locator, timeout=appear_timeout)
        resolved_locator = self._resolve_locator(locator)
        await resolved_locator.wait_for(
            state="hidden", timeout=disappear_timeout * 1000
        )
        return True

    async def verify_element_text(
        self, locator: Union[Locator, str], expected_text: str
    ):
        actual_text = await self.get_element_text(locator)
        return actual_text == expected_text

    async def verify_element_visible(self, locator: Union[Locator, str]):
        return await self.is_element_visible(locator)

    async def scroll_to_element(self, locator: Union[Locator, str]):
        """
        Note: Playwright's scroll_into_view_if_needed() automatically waits for element to be attached to DOM.
        """
        resolved_locator = self._resolve_locator(locator)
        await resolved_locator.scroll_into_view_if_needed()
        return resolved_locator

    async def wait_for_element_disappears(
        self, locator: Union[Locator, str], timeout=10
    ):
        try:
            resolved_locator = self._resolve_locator(locator)
            await resolved_locator.wait_for(state="hidden", timeout=timeout * 1000)
            return True
        except PlaywrightTimeoutError:
            raise AssertionError(
                f"Element does not disappear in {timeout} seconds: {locator}"
            )

    async def refresh_page(self):
        await self.page.reload(wait_until="networkidle")

    async def refresh_and_wait_for_element(
        self, locator: Union[Locator, str], timeout=10
    ):
        await self.page.reload(wait_until="networkidle")
        resolved_locator = self._resolve_locator(locator)
        await resolved_locator.wait_for(state="visible", timeout=timeout * 1000)

    async def wait_for_element_has_value(
        self, locator: Union[Locator, str], timeout=10
    ):
        await self.wait_for_element_visible(locator)

        resolved_locator = self._resolve_locator(locator)

        import time

        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                current_value = await resolved_locator.input_value()
                if current_value and current_value.strip():
                    return True
            except Exception:
                pass
            await self.page.wait_for_timeout(100)

        raise PlaywrightTimeoutError(
            f"Element in {timeout} seconds did not get a value: {locator}"
        )

    async def switch_to_new_window(self, timeout=10):
        original_page = self.page
        context = self.page.context

        import time

        end_time = time.time() + timeout
        while time.time() < end_time:
            pages = context.pages
            if len(pages) > 1:
                for page in pages:
                    if page != original_page and not page.is_closed():
                        await page.bring_to_front()
                        await page.wait_for_load_state("domcontentloaded")
                        await page.wait_for_load_state("load")
                        return page
            await self.page.wait_for_timeout(500)

        raise PlaywrightTimeoutError(f"在 {timeout} 秒內未檢測到新窗口打開")

    async def close_current_window_and_switch_back(self, original_page: Page):
        context = self.page.context
        new_page = None
        for page in context.pages:
            if page != original_page and not page.is_closed():
                new_page = page
                break
        if new_page and not new_page.is_closed():
            await new_page.close()
        self.page = original_page
        try:
            if original_page.is_closed():
                raise ValueError("原視窗已關閉")
            await original_page.bring_to_front()
            await original_page.wait_for_load_state("domcontentloaded", timeout=5000)
            await original_page.wait_for_load_state("load", timeout=5000)
            await original_page.wait_for_timeout(500)
        except Exception as e:
            print(f"警告：等待原視窗載入時出現問題: {e}")
            if not original_page.is_closed():
                await original_page.bring_to_front()
                await original_page.wait_for_timeout(1000)
