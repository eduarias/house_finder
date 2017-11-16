from behave import when, then, register_type

import parse


@parse.with_pattern(r'.*')
def parse_list(text):
    return text.split(', ')


register_type(Columns=parse_list)


@when('user goes to homepage')
def homepage(context):
    context.browser.visit(context.base_url)


@then('it should contains a table with houses')
def contains_table(context):
    table_elements = context.browser.find_by_id('houses-tables')
    context.test.assertEqual(1, len(table_elements))


@then('table contains columns: {columns:Columns}')
def contains_columns(context, columns):
    for column in columns:
        table_header = context.browser.find_by_id('header-{}'.format(column))
        context.test.assertEqual(1, len(table_header), msg='Column {} not found'.format(column))