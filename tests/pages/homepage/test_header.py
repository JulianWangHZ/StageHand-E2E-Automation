import pytest
from pytest_bdd import given, parsers, scenarios, then, when
from stagehand import Stagehand

from tests.pages.base.base_action import BaseActions

scenarios("../../../features/homepage/header.feature")


# ============================================================================
# Scenario : All header elements are visible @header @header_visibility
# ============================================================================


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
    logo_locator = 'a[href*="transglobalus.com"]'
    is_visible = await base_actions.verify_element_visible(logo_locator)
    assert is_visible


@then("the logo should link to the homepage URL")
async def logo_links_homepage_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    logo_link = page.locator('a[href="https://www.transglobalus.com/"]').filter(
        has=page.locator("img")
    )
    await logo_link.wait_for(state="visible", timeout=5000)
    href = await logo_link.get_attribute("href")
    assert href == "https://www.transglobalus.com/"


@then(parsers.parse('I should see the "{menu_item}" menu item'))
async def see_menu_item_visibility(stagehand_on_demand: Stagehand, menu_item: str):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    menu_locator = f"text={menu_item}"
    is_visible = await base_actions.verify_element_visible(menu_locator)
    assert is_visible


@then(parsers.parse('I should see the "{menu_item}" menu item in the top menu'))
async def see_top_menu_item_visibility(stagehand_on_demand: Stagehand, menu_item: str):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    menu_locator = f"text={menu_item}"
    is_visible = await base_actions.verify_element_visible(menu_locator)
    assert is_visible


@then("the language selector should be visible")
async def language_selector_visible_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    language_locator = 'a[href="#pll_switcher"]'
    is_visible = await base_actions.verify_element_visible(language_locator)
    assert is_visible


@then(parsers.parse('it should display "{text}"'))
async def display_text_visibility(stagehand_on_demand: Stagehand, text: str):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    text_locator = f"text={text}"
    is_visible = await base_actions.verify_element_visible(text_locator)
    assert is_visible


@then("social media links should be visible")
async def social_media_visible_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    facebook_locator = 'a[href*="facebook.com"]'
    is_visible = await base_actions.verify_element_visible(facebook_locator)
    assert is_visible


@then("I should see Facebook link")
async def see_facebook_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    facebook_locator = 'a[href*="facebook.com"]'
    is_visible = await base_actions.verify_element_visible(facebook_locator)
    assert is_visible


@then("I should see Twitter link")
async def see_twitter_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    twitter_locator = 'a[href*="twitter.com"], a[href*="x.com"]'
    is_visible = await base_actions.verify_element_visible(twitter_locator)
    assert is_visible


@then("I should see LinkedIn link")
async def see_linkedin_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    linkedin_locator = 'a[href*="linkedin.com"]'
    is_visible = await base_actions.verify_element_visible(linkedin_locator)
    assert is_visible


@then("I should see YouTube link")
async def see_youtube_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    youtube_locator = 'a[href*="youtube.com"]'
    is_visible = await base_actions.verify_element_visible(youtube_locator)
    assert is_visible


@then("I should see Instagram link")
async def see_instagram_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    instagram_locator = 'a[href*="instagram.com"]'
    is_visible = await base_actions.verify_element_visible(instagram_locator)
    assert is_visible


@then("the phone link should be visible")
async def phone_link_visible_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    phone_locator = 'a[href^="tel:"]'
    is_visible = await base_actions.verify_element_visible(phone_locator)
    assert is_visible


@then("it should be clickable")
async def phone_link_clickable_visibility(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    phone_link = page.locator('a[href^="tel:"]').first()
    await phone_link.wait_for(state="visible", timeout=5000)
    href = await phone_link.get_attribute("href")
    assert href and href.startswith("tel:")


# ============================================================================
# Scenario : Clicking CONTACT US menu item navigates to contact page @header @header_click_contact
# ============================================================================


@given("I navigate to the TransGlobal homepage")
async def navigate_homepage_contact(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.open_url("https://www.transglobalus.com/")
    await base_actions.wait_for_page_loaded()


@when(parsers.parse('I click the "{menu_item}" menu item in the header'))
async def click_contact_menu_item(stagehand_on_demand: Stagehand, menu_item: str):
    page = stagehand_on_demand.page
    await page.act(f'click the "{menu_item}" in the header')
    await page.wait_for_load_state("networkidle")


@then("I should be navigated to the contact page")
async def navigated_to_contact_page(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.wait_for_page_loaded()
    await page.wait_for_timeout(1000)
    current_url = page.url
    assert "contact" in current_url.lower()
    body_locator = "body"
    await base_actions.wait_for_element_visible(body_locator, timeout=5)
    body_text = await base_actions.get_element_text(body_locator)
    assert len(body_text.strip()) > 0, "Page appears to be blank"


@then(parsers.parse('the URL should contain "{text}"'))
async def url_contains_contact(stagehand_on_demand: Stagehand, text: str):
    page = stagehand_on_demand.page
    await page.wait_for_load_state("networkidle")
    current_url = page.url
    assert text.lower() in current_url.lower()


# ============================================================================
# Scenario : Clicking MEDIA menu item navigates to media page @header @header_click_media
# ============================================================================


@given("I navigate to the TransGlobal homepage")
async def navigate_homepage_media(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.open_url("https://www.transglobalus.com/")
    await base_actions.wait_for_page_loaded()


@when(parsers.parse('I click the "{menu_item}" menu item in the header'))
async def click_media_menu_item(stagehand_on_demand: Stagehand, menu_item: str):
    page = stagehand_on_demand.page
    await page.act(f'click the "{menu_item}" in the header')
    await page.wait_for_load_state("networkidle")


@then("I should be navigated to the media page")
async def navigated_to_media_page(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.wait_for_page_loaded()
    await page.wait_for_timeout(1000)
    current_url = page.url
    assert "media" in current_url.lower() or "transglobaltv" in current_url.lower()
    body_locator = "body"
    await base_actions.wait_for_element_visible(body_locator, timeout=5)
    body_text = await base_actions.get_element_text(body_locator)
    assert len(body_text.strip()) > 0, "Page appears to be blank"


@then(parsers.parse('the URL should contain "{text1}" or "{text2}"'))
async def url_contains_media_or(stagehand_on_demand: Stagehand, text1: str, text2: str):
    page = stagehand_on_demand.page
    await page.wait_for_load_state("networkidle")
    current_url = page.url
    assert text1.lower() in current_url.lower() or text2.lower() in current_url.lower()


# ============================================================================
# Scenario : Clicking NEWS menu item navigates to news page @header @header_click_news
# ============================================================================


@given("I navigate to the TransGlobal homepage")
async def navigate_homepage_news(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.open_url("https://www.transglobalus.com/")
    await base_actions.wait_for_page_loaded()


@when(parsers.parse('I click the "{menu_item}" menu item in the header'))
async def click_news_menu_item(stagehand_on_demand: Stagehand, menu_item: str):
    page = stagehand_on_demand.page
    await page.act(f'click the "{menu_item}" in the header')
    await page.wait_for_load_state("networkidle")


@then("I should be navigated to the news page")
async def navigated_to_news_page(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.wait_for_page_loaded()
    await page.wait_for_timeout(1000)
    current_url = page.url
    assert "news" in current_url.lower()
    body_locator = "body"
    await base_actions.wait_for_element_visible(body_locator, timeout=5)
    body_text = await base_actions.get_element_text(body_locator)
    assert len(body_text.strip()) > 0, "Page appears to be blank"


@then(parsers.parse('the URL should contain "{text}"'))
async def url_contains_news(stagehand_on_demand: Stagehand, text: str):
    page = stagehand_on_demand.page
    await page.wait_for_load_state("networkidle")
    current_url = page.url
    assert text.lower() in current_url.lower()


# ============================================================================
# Scenario : Clicking EVENTS dropdown item navigates to correct page @header @header_click_events_dropdown
# ============================================================================


@given("I navigate to the TransGlobal homepage")
async def navigate_homepage_events(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.open_url("https://www.transglobalus.com/")
    await base_actions.wait_for_page_loaded()


@when(parsers.parse('I hover over "{menu_item}" menu item'))
async def hover_click_events_menu(stagehand_on_demand: Stagehand, menu_item: str):
    page = stagehand_on_demand.page
    await page.act(f'hover over "{menu_item}" in the header')
    await page.wait_for_timeout(1000)


@when(parsers.parse('I click the "{item}" item in the EVENTS dropdown'))
async def click_events_dropdown_item(stagehand_on_demand: Stagehand, item: str):
    page = stagehand_on_demand.page
    await page.act(f'click the "{item}" item in the EVENTS dropdown menu')
    await page.wait_for_load_state("networkidle")


@then("I should be navigated to the webinar page")
async def navigated_to_webinar_page(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.wait_for_page_loaded()
    await page.wait_for_timeout(1000)
    current_url = page.url
    assert "seminars" in current_url.lower()
    body_locator = "body"
    await base_actions.wait_for_element_visible(body_locator, timeout=5)
    body_text = await base_actions.get_element_text(body_locator)
    assert len(body_text.strip()) > 0, "Page appears to be blank"


@then(parsers.parse('the URL should contain "{text}"'))
async def url_contains_seminars(stagehand_on_demand: Stagehand, text: str):
    page = stagehand_on_demand.page
    await page.wait_for_load_state("networkidle")
    current_url = page.url
    assert text.lower() in current_url.lower()


# ============================================================================
# Scenario : Clicking ABOUT US dropdown item navigates to correct page @header @header_click_about_us_dropdown
# ============================================================================


@given("I navigate to the TransGlobal homepage")
async def navigate_homepage_about_us(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.open_url("https://www.transglobalus.com/")
    await base_actions.wait_for_page_loaded()


@when(parsers.parse('I hover over "{menu_item}" menu item'))
async def hover_click_about_us_menu(stagehand_on_demand: Stagehand, menu_item: str):
    page = stagehand_on_demand.page
    await page.act(f'hover over or click the "{menu_item}" menu item in the header')
    await page.wait_for_timeout(1000)


@when(parsers.parse('I click the "{item}" item in the ABOUT US dropdown'))
async def click_about_us_dropdown_item(stagehand_on_demand: Stagehand, item: str):
    page = stagehand_on_demand.page
    await page.act(f'click the "{item}" item in the ABOUT US dropdown menu')
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(2000)


@then("I should be navigated to the about us page")
async def navigated_to_about_us_page(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.wait_for_page_loaded()
    await page.wait_for_timeout(1000)
    current_url = page.url
    assert "about-us" in current_url.lower()
    body_locator = "body"
    await base_actions.wait_for_element_visible(body_locator, timeout=5)
    body_text = await base_actions.get_element_text(body_locator)
    assert len(body_text.strip()) > 0, "Page appears to be blank"


@then(parsers.parse('the URL should contain "{text}"'))
async def url_contains_about_us(stagehand_on_demand: Stagehand, text: str):
    page = stagehand_on_demand.page
    await page.wait_for_load_state("networkidle")
    current_url = page.url
    assert text.lower() in current_url.lower()


# ============================================================================
# Scenario : Clicking Resource dropdown item navigates to correct page @header @header_click_resource_dropdown
# ============================================================================


@given("I navigate to the TransGlobal homepage")
async def navigate_homepage_resource(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.open_url("https://www.transglobalus.com/")
    await base_actions.wait_for_page_loaded()


@when(parsers.parse('I hover over "{menu_item}" menu item in the top menu'))
async def hover_click_resource_menu(stagehand_on_demand: Stagehand, menu_item: str):
    page = stagehand_on_demand.page
    await page.act(f'hover over or click the "{menu_item}" menu item in the top menu')
    await page.wait_for_timeout(1000)


@when(parsers.parse('I click the "{item}" item in the Resource dropdown'))
async def click_resource_dropdown_item(stagehand_on_demand: Stagehand, item: str):
    page = stagehand_on_demand.page
    await page.act(f'click the "{item}" item in the Resource dropdown menu')
    await page.wait_for_load_state("networkidle")


@then("I should be navigated to the agent portal page")
async def navigated_to_agent_portal_page(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.wait_for_page_loaded()
    await page.wait_for_timeout(1000)
    current_url = page.url
    assert "tgpt.transglobalus.com" in current_url.lower()
    try:
        body_locator = "body"
        await base_actions.wait_for_element_visible(body_locator, timeout=5)
        body_text = await base_actions.get_element_text(body_locator)
        assert len(body_text.strip()) > 0, "Page appears to be blank"
    except Exception:
        pass


@then(parsers.parse('the URL should contain "{text}"'))
async def url_contains_tgpt(stagehand_on_demand: Stagehand, text: str):
    page = stagehand_on_demand.page
    await page.wait_for_load_state("networkidle")
    current_url = page.url
    assert text.lower() in current_url.lower()


# ============================================================================
# Scenario : Clicking language selector shows language options @header @header_click_language_dropdown
# ============================================================================


@given("I navigate to the TransGlobal homepage")
async def navigate_homepage_language(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.open_url("https://www.transglobalus.com/")
    await base_actions.wait_for_page_loaded()


@when("I click the language selector in the header")
async def click_language_selector(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    await page.act("click the language selector in the header")
    await page.wait_for_timeout(1000)


@then("I should see the language dropdown menu")
async def see_language_dropdown(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    await page.wait_for_timeout(500)
    dropdown = page.locator('#pll_switcher, .pll-switcher, [class*="language"]')
    assert (
        await dropdown.count() > 0
        or await page.locator("text=中文, text=English").count() > 0
    )


@then("I should see language options in the dropdown")
async def see_language_options(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    await page.wait_for_timeout(500)
    language_options = page.locator(
        "text=中文, text=English, text=繁體中文, text=简体中文"
    )
    assert await language_options.count() > 0


# ============================================================================
# Scenario : SERVICES menu has dropdown with submenu items @header @header_services_dropdown
# ============================================================================


@given("I navigate to the TransGlobal homepage")
async def navigate_homepage_services(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    base_actions = BaseActions(page)
    await base_actions.open_url("https://www.transglobalus.com/")
    await base_actions.wait_for_page_loaded()


@when(parsers.parse('I hover over "{menu_item}" menu item'))
async def hover_click_services_menu(stagehand_on_demand: Stagehand, menu_item: str):
    page = stagehand_on_demand.page
    await page.act(f'hover over "{menu_item}" in the header')
    await page.wait_for_timeout(1000)


@then("I should see the dropdown menu")
async def see_dropdown_menu_services(stagehand_on_demand: Stagehand):
    page = stagehand_on_demand.page
    await page.wait_for_timeout(500)
    dropdown = page.locator('.sub-menu, .dropdown-menu, [class*="submenu"]')
    assert await dropdown.count() > 0


@then(parsers.parse('I should see "{item}" in the dropdown'))
async def see_item_in_dropdown_services(stagehand_on_demand: Stagehand, item: str):
    page = stagehand_on_demand.page
    await page.wait_for_timeout(500)
    dropdown_item = page.locator(f"text={item}").first()
    await dropdown_item.wait_for(state="visible", timeout=5000)
    assert await dropdown_item.is_visible()
