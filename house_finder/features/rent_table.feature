Feature: Houses for rent table
  In order to be able to read data gathered by crawler
  As a user
  I want a table with the houses

  Scenario: Table contains houses from database
    Given user has an open browser
     When opening the homepage
     Then the homepage contains a table with houses