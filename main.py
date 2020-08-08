from selenium import webdriver
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time
import os
from datetime import timedelta, datetime

def main():
    browserIsOpen = True
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    browser = webdriver.Chrome(os.path.dirname(os.path.realpath(__file__)) + "/chromedriver", options=chrome_options)

    try:
        print("Collecting data...")
        browser.get("https://www.foreca.fi/Finland/Ylojarvi/10vrk")

        # ----------------------------------------------

        day = browser.find_elements_by_xpath("//div[@class='day']/a/h5")
        weather = browser.find_elements_by_xpath("//div[@class='day']/a/div/p[1]/span[@class='warm']")

        browserIsOpen = False

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

        print("\u001b[32mDisplaying results...\u001b[0m")
        sns.set()
        _, ax = plt.subplots(1)
        xdata = []
        ydata = []

        text_values = []    # Week days to be displayed at the bottom of the diagram
        for _ in days:
            day = _
            while len(day) > 2:
                day = day[:-1]
            text_values.append(day)
        x_values = np.arange(0, len(text_values), 1)

        for _ in range(0, len(days)):
            xdata.append(_)

        for _ in days:
            ydata.append(int(days[_]))
        
        ax.plot(xdata, ydata, color="red")
        ax.set_ylim(ymin=0)
        plt.title("10 Days Forecast (" + datetime.now().strftime("%d") + " - " + (datetime.now()+timedelta(days=10)).strftime("%d.%m") + ")")
        plt.ylabel("Celcius °C")
        plt.xticks(np.arange(min(xdata), max(xdata)+1, 1.0))
        plt.xticks(x_values, text_values)
        plt.show()

        # plt.savefig("forecast_" + datetime.now().strftime("%d") + "-" + (datetime.now()+timedelta(days=10)).strftime("%d.%m") + ".jpg")

    except(KeyboardInterrupt):
        if browserIsOpen:
            browser.quit()

        print("\u001b[31m Process interrupted!\u001b[0m")
        quit()

main()