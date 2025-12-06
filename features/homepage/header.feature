Feature: Header functionality on homepage
  As a user
  I want to interact with the header elements on the TransGlobal website
  So that I can navigate and access different sections of the website

  @header @header_visibility
  Scenario: All header elements are visible
    Given I navigate to the TransGlobal homepage
    When I look at the header
    Then the TransGlobal logo should be visible
    And the logo should link to the homepage URL
    And I should see the "SERVICES" menu item
    And I should see the "EVENTS" menu item
    And I should see the "MEDIA" menu item
    And I should see the "NEWS" menu item
    And I should see the "ABOUT US" menu item
    And I should see the "CONTACT US" menu item
    And I should see the "Resource" menu item in the top menu
    And the language selector should be visible
    And it should display "English"
    And social media links should be visible
    And I should see Facebook link
    And I should see Twitter link
    And I should see LinkedIn link
    And I should see YouTube link
    And I should see Instagram link
    And the phone link should be visible
    And it should be clickable


  @header @header_click_contact
  Scenario: Clicking CONTACT US menu item navigates to contact page
    Given I navigate to the TransGlobal homepage
    When I click the "CONTACT US" menu item in the header
    Then I should be navigated to the contact page
    And the URL should contain "contact"

  @header @header_click_media
  Scenario: Clicking MEDIA menu item navigates to media page
    Given I navigate to the TransGlobal homepage
    When I click the "MEDIA" menu item in the header
    Then I should be navigated to the media page
    And the URL should contain "media" or "transglobaltv"

  @header @header_click_news
  Scenario: Clicking NEWS menu item navigates to news page
    Given I navigate to the TransGlobal homepage
    When I click the "NEWS" menu item in the header
    Then I should be navigated to the news page
    And the URL should contain "news"

  @header @header_click_events_dropdown
  Scenario: Clicking EVENTS dropdown item navigates to correct page
    Given I navigate to the TransGlobal homepage
    When I hover over "EVENTS" menu item
    And I click the "Webinar" item in the EVENTS dropdown
    Then I should be navigated to the webinar page
    And the URL should contain "seminars"

  @header @header_click_about_us_dropdown
  Scenario: Clicking ABOUT US dropdown item navigates to correct page
    Given I navigate to the TransGlobal homepage
    When I hover over "ABOUT US" menu item
    And I click the "Our Story" item in the ABOUT US dropdown
    Then I should be navigated to the about us page
    And the URL should contain "about-us"

  @header @header_click_resource_dropdown
  Scenario: Clicking Resource dropdown item navigates to correct page
    Given I navigate to the TransGlobal homepage
    When I hover over "Resource" menu item in the top menu
    And I click the "Agent Portal" item in the Resource dropdown
    Then I should be navigated to the agent portal page
    And the URL should contain "tgpt.transglobalus.com"

  @header @header_click_language_dropdown
  Scenario: Clicking language selector shows language options
    Given I navigate to the TransGlobal homepage
    When I click the language selector in the header
    Then I should see the language dropdown menu
    And I should see language options in the dropdown

  @header @header_services_dropdown
  Scenario: SERVICES menu has dropdown with submenu items
    Given I navigate to the TransGlobal homepage
    When I hover over "SERVICES" menu item
    Then I should see the dropdown menu
    And I should see "Real Estate" in the dropdown
    And I should see "Lending" in the dropdown
    And I should see "Insurance" in the dropdown
    And I should see "Investment" in the dropdown
    And I should see "Tax" in the dropdown
