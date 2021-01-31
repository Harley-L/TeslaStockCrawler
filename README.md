# TeslaStockCrawler
A web crawler that searches for the correlation between past news headlines and changes in stock prices. Can predict the
change in stock price from only looking at today's news.

## Usage
First, pull this repository using:
````
git pull https://github.com/Harley-L/TeslaStockCrawler.git
````
After setting up the repository, there are a couple of parameters that can be changed. If you want to create new data 
refer to the **Create Data** section. If you have recently created your data and want faster results, refer to the **Use 
Old Data** section.

### Create Data
If this is the first time running this program or want to update the data, you have come to the right place! First, 
update the *dayDifference* parameter. This can be found on line 9 of *main.py* and is an integer that represents how 
long ago the program goes back in history to look at the stock.

After updating the length of time, you have to enable collecting the data. This can be found on line 102 where 
*updateData* is set to a boolean value. Set *updateData* to *True*.

Although not recommended, it is possible to run this program without the *headless* feature. This would allow you to see
the bot going to each webpage and may slow down the program. Changing this feature is found on lines 53 and 136 where 
the boolean value is preset to *True*. Line 53 and 136 changes the *headless* of the data collection and today's news 
respectively. 

### Use Old Data
If you would like to run this program off of previously collected data, the only parameter that needs to be set is 
*updateData*. Set *updateData* to *False*.

See above in the **Create Data** section for details about the *headless* feature

### Output
The output of the program is three lines. One to say the price change of the most recent date the stock market was open.
The program **does not see this information**. The second line is the prediction where the algorithm either predicts if
the stock *increased* or *decreased* that most recent date. The last line is the generated coefficient. If the 
coefficient is positive, the algorithm predicted a positive change and vise versa. The magnitude of the coefficient 
**does not equate to a dollar value**.

## How It Works
For each day the stock market is open, the program web-scrapes to get all of the TSLA-specific headlines for that day 
and multiplies the frequency of the word by the change in stock price. This repository primarily uses Selenium in 
combination with BeautifulSoup to web-scrape and collect word frequencies. Collecting the stock price for that day 
relied on the yfinance package. After collecting this data and putting it into a large dictionary, the program transfers 
the data into a CSV for usage without running the collected data.

Lastly, the program finds the headlines for the present-day and if a word is in the previous dictionary, it adds the 
words value to the coefficient.

This program was super fun and interesting to build but it is very biased. Due to TSLA increasing an astronomical 
amount, general words that are normally found in headlines such as "Tesla" have very large positive values associated 
with them. Upon the next iteration of this program, I will introduce a mean value to even out this disparity.