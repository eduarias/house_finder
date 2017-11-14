from splinter.browser import Browser


def before_all(context):
    print("")
    print("> Starting the browser")
    context.browser = Browser('firefox', headless=True)


def after_all(context):
    print("< Closing the browser")
    print("")
    context.browser.quit()
    context.browser = None
