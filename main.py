from selenium import webdriver
import selenium
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
        browser.get("https://www.foreca.fi/Finland/Ylöjärvi/10vrk")

        # ----------------------------------------------

        day = browser.find_elements_by_xpath("//div[@class='day']/a/h5")
        temperature_high = browser.find_elements_by_xpath("//div[@class='day']/a/div/p[1]/span[@class='warm']")
        temperature_low = browser.find_elements_by_xpath("//div[@class='day']/a/div/p[2]/span[@class='warm']")
        city = browser.find_element_by_xpath("//div[@class='navihead']/h2/a").text

        # -----------------------------------------------

        print("Processing data...")
        days = {}
        days_cold = {}
        for date, warmth_high, warmth_low in zip(day, temperature_high, temperature_low):
            high = warmth_high.text
            low = warmth_low.text

            # Removing +/- and °
            high = high[1:]
            high = high[:-1]
            low = low[1:]
            low = low[:-1]

            days[date.text] = int(high)
            days_cold[date.text] = int(low)

        browserIsOpen = False
        browser.close()

        # -----------------------------------------------

        print("\u001b[32mDisplaying results...\u001b[0m")
        sns.set()

        _, ax = plt.subplots(1)
        xdata = []
        ydata = []
        ydata2 = []

        text_values = []    # Week days to be displayed at the bottom of the diagram
        for _ in days:
            day = _
            while len(day) > 2:
                day = day[:-1]
            text_values.append(day)
        x_values = np.arange(0, len(text_values), 1)

        # Warm
        for _ in range(0, len(days)):
            xdata.append(_)

        for _ in days:
            ydata.append(int(days[_]))

        # Cold
        for _ in days_cold:
            ydata2.append(int(days_cold[_]))

        # -----------------------------------------------
        
        # Display results
        ax.plot(xdata, ydata, color="red")
        ax.plot(xdata, ydata2, color="blue")

        ax.set_ylim(ymin=0)
        plt.title("10 Päivän Ennuste (" + datetime.now().strftime("%d") + " - " + (datetime.now()+timedelta(days=9)).strftime("%d.%m") + ")\n" + city)
        plt.ylabel("Celcius °C")
        plt.xticks(np.arange(min(xdata), max(xdata)+1, 1.0))
        plt.xticks(x_values, text_values)
        plt.show()


    except(KeyboardInterrupt):
        if browserIsOpen:
            browser.quit()

        print("\u001b[31m Process interrupted!\u001b[0m")
        quit()

main()