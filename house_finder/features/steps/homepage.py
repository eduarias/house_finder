from time import sleep

from behave import given, when, then
from selenium import webdriver

URL = 'http://localhost:8000/'


@given('user has an open browser')
def step_impl(context):
    context.browser = webdriver.Chrome()


@when('opening the homepage')
def step_impl(context):
    context.browser.get(URL)


@then('the homepage contains a table with houses')
def step_impl(context):
    context.browser.
