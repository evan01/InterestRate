from selenium import webdriver

def takeScreenShot(url):
    '''
    This function will take a screenshot of a website with a given url
    :return:
    '''
    #depot = DepotManager.get()
    driver = webdriver.PhantomJS()
    driver.set_window_size(1024, 768)  # set the window size that you need
    driver.get(url)
    driver.save_screenshot("temp.png")


if __name__ == '__main__':
    takeScreenShot("a")