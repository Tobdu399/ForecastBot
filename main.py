from selenium import webdriver
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time
import os

def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")

    print("Collecting data...")
    browser = webdriver.Chrome(os.path.dirname(os.path.realpath(__file__)) + "/chromedriver", options=chrome_options)
    browser.get("https://www.foreca.fi/Finland/Ylojarvi/10vrk")

    # ----------------------------------------------

    day = browser.find_elements_by_xpath("//div[@class='day']/a/h5")
    weather = browser.find_elements_by_xpath("//div[@class='day']/a/div/p[1]/span[@class='warm']")

    print("Processing data...")
    days = {}
    for date, warmth in zip(day, weather):
        _ = warmth.text

        # Removing +/- and °
        _ = _[1:]
        _ = _[:-1]

        days[date.text] = int(_)

    browser.close()

    # -----------------------------------------------

    print("Displaying results...")
    sns.set()
    _, ax = plt.subplots(1)
    xdata = []
    ydata = []

    for _ in range(0, len(days)):
        xdata.append(_)

    for _ in days:
        ydata.append(int(days[_]))
    
    ax.plot(xdata, ydata)
    ax.set_ylim(ymin=0)
    plt.title("10 Days Forecast")
    plt.ylabel("Celcius °C")
    plt.xticks(np.arange(min(xdata), max(xdata)+1, 1.0))
    plt.show()


main()