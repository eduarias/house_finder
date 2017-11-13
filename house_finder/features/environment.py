from splinter.browser import Browser
from xvfbwrapper import Xvfb


def before_all(context):
    print("")
    context.vdisplay = Xvfb()
    context.vdisplay.start()
    print("> Starting the browser")
    context.browser = Browser('chrome')


def after_all(context):
    print("< Closing the browser")
    print("")
    context.browser.quit()
    context.browser = None
    context.vdisplay.stop()
