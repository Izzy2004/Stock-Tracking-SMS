# Stock-Tracking-SMS

Pulls candlestick values from Alpha Vantage API and locates all articles from the past few days for that company if stock volatility is high enough. 

Sorts articles by relevance and splices the top three into a list, which is then formatted to be displayed as SMS message.

SMS containing a percent increase, article header, and description is sent to the designated number.
