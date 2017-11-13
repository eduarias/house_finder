Feature: Houses for rent table
  In order to be able to read data gathered by crawler
  As a user
  I want a table with the houses

  Scenario: Table contains houses from database
     When user goes to homepage
     Then the homepage should contains a table with houses