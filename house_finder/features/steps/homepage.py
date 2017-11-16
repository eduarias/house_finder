from behave import when, then


@when('user goes to homepage')
def homepage(context):
    context.browser.visit(context.base_url)


@then('it should contains a table with houses')
def contains_table(context):
    table_elements = context.browser.find_by_id('houses-tables')
    context.test.assertEqual(1, len(table_elements))
