Feature: Houses for rent table
  In order to be able to read data gathered by crawler
  As a user
  I want a table with the houses

  Scenario: Table contains houses from database
     When user goes to homepage
     Then it should contains a table with houses
     And table contains columns: title, neighborhood, price, m2, rooms, baths, url


Feature: Filtering
  In order to refine a search
  As I user
  I want to be able to filter the results

  Scenario: Filter is in homepage
    When user goes to homepage
    Then there should be a filter option