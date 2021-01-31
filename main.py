import yfinance as yf
from datetime import date, datetime, timedelta  # find todays date (as a timestamp)
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

# Set how long it looks in the past
dayDifference = 3*365
farthestTime = datetime.strftime((datetime.now() - timedelta(dayDifference)), '%Y-%m-%d')

# Get stock proces from the last X amount of time using the yfinance library
tickerSymbol = 'TSLA'
# get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
# get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start=str(farthestTime), end='2121-1-13')
# Get the difference in stock price
finalDf = tickerDf["Close"] - tickerDf["Open"]
dt = date.today()
today = datetime.combine(dt, datetime.min.time())
stockDict = finalDf.to_dict()


def slicer(startstring, endstring, string):  # Helper function to parse HTML and find titles of articles
    global titles

    title = ''
    index = string.find(startstring)
    if index != -1:
        string = string[index + len(startstring):]
    else:
        return 1
    for char in range(200):
        if string[char] == endstring:
            titles += title + ' '
            return slicer(startstring, endstring, string)
        else:
            title += string[char]
    return 1


# Calculate stock/news past 2 years (NOT INCLUDING TODAY) -- Goal: Update wordDict every day
def calcPastData():
    # Definitions
    global titles
    titles = ''
    wordDict = {}

    # Inialize the Headless driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    headless = True  # CHANGE HERE if want to see the driver with head
    if headless is True:
        driver = webdriver.Chrome('C:/Users/harle/Documents/chromedriver', options=chrome_options)
    else:
        driver = webdriver.Chrome('C:/Users/harle/Documents/chromedriver')

    wordDict = {}
    counter = 0
    for date in stockDict.keys():  # For each date, load browser, get headlines, and add words with stock data to dict
        day = date.day
        month = date.month
        year = date.year

        # Load browser
        google_url = f"https://www.google.com/search?q=tesla&rlz=1C1CHBF_enCA926CA926&biw=1011&bih=896&tbas=0&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{month}%2F{day}%2F{year}%2Ccd_max%3A{month}%2F{day}%2F{year}&tbm=nws"
        driver.get(google_url)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        result_div = soup.find_all('div', attrs={'class': 'JheGif nDgy9d'})

        html = ''

        # Parse HTML
        for i in range(len(result_div)):
            html += str(result_div[i])
        startstring = "style=\"-webkit-line-clamp:2\">"
        endstring = "<"
        slicer(startstring, endstring, html)

        # Get stock price for the day
        stocktoday = stockDict[date]

        # Break up titles into words and assign them values for frequency
        words = titles.split()
        for word in words:
            if word in wordDict:
                wordDict[word] += stocktoday
            else:
                wordDict[word] = stocktoday
        counter += 1
        percentDone = round(counter/len(stockDict), 4)
        print(f"Collecting Data: {counter}/{len(stockDict)}", end=" ")
        print("{0:.2f}%".format(percentDone*100))
    return wordDict


# UPDATE THE STOCK DATA OR JUST LOOK AT THE CSV FILE
updateData = False  # Modifier - Change if reading CSV or getting new data

if updateData == True:
    historicalData = calcPastData()

    with open('dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in historicalData.items():
           try:
               writer.writerow([key, value])
           except:
               pass
else:
    historicalData = {}
    with open('dict.csv') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            try:
                historicalData[row[0]] = row[1]
            except:
                pass


def calcEstimate(wordDict,todayDate):  # Calculate todays estimate
    global titles
    titles = ''
    todayEstimate = 0
    day = todayDate[8:]
    month = todayDate[5:7]
    year = todayDate[:4]

    # Load driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    headless = True  # CHANGE if want top see head of browser

    if headless is True:
        driver = webdriver.Chrome('C:/Users/harle/Documents/chromedriver', options=chrome_options)
    else:
        driver = webdriver.Chrome('C:/Users/harle/Documents/chromedriver')

    google_url = f"https://www.google.com/search?q=tesla&rlz=1C1CHBF_enCA926CA926&biw=1011&bih=896&tbas=0&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{month}%2F{day}%2F{year}%2Ccd_max%3A{month}%2F{day}%2F{year}&tbm=nws"
    driver.get(google_url)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    result_div = soup.find_all('div', attrs={'class': 'JheGif nDgy9d'})

    html = ''

    # HTML Parsing
    for i in range(len(result_div)):
        html += str(result_div[i])
    startstring = "style=\"-webkit-line-clamp:2\">"
    endstring = "<"
    slicer(startstring, endstring, html)

    # Break up titles into words and assign them values for frequency
    headlineToday = titles.split()
    for words in headlineToday:
        if words in wordDict:
            todayEstimate += float(wordDict[words])
    return todayEstimate

todayPrice = list(stockDict)[-1]
todayDate =str(list(stockDict)[-1])[:10]

todayEstimate = calcEstimate(historicalData, todayDate)

# Output.
print(f"TSLA changed price by {stockDict[todayPrice]} on {todayDate}")
if todayEstimate > 0:
    print("The algorithm predicts that TSLA INCREASED in price today")
else:
    print("The algorithm predicts that TSLA DECREASED in price today")
print(f"Generated coefficient: {todayEstimate}")
