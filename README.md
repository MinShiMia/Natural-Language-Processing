# Introduction
This repository contains the codes of natural language processing project -- Predicting the Changes of S&P 500 Stock Price based on 
WSJ News Articles – NLP & ML Approaches.

The media outlets, such as newspapers, play an imperative role in disseminating information to a broad audience. The audience replies to news to understand events and make further actions. Till today, newspapers have a large and loyal base of readers. Specifically, 58% of adults aged 18-34 and 60% aged over 35 read a newspaper (MANS Media, 2022). The Wall Street Journal (WSJ) is an American business-focused, international daily newspaper, one of the largest newspapers in the U.S. by circulation (Wikipedia Foundation, 2022b). The news articles covered by WSJ represent the breaking news and the tendency in the world.

The stock index reflects how the stock market is and how good the companies’ operations status is. The Standard and Poor’s 500 (S&P 500) is a stock market index tracking the stock performances of 500 large companies listed on the stock exchanges in the U.S. and is one of the most followed equity indices (Wikipedia Foundation, 2022a).

The U.S. is the world’s largest economy and the largest exporter and importer of goods and services. Trade is critical to U.S. companies’ operations since most U.S. companies rely on imports for their materials supplement and export to sell their products or services globally.
In this project, I investigate the WSJ news articles related to “U.S. trade” and use the matrix of token counts generated by Count Vectorizer, Tfidf Vectorizer, and n-grams Count Vectorizer from the collection of news article text to predict how the U.S. stock market and U.S. companies operate measured by S&P 500 stock index.
 
# Datasets 
The news articles are scraped from the Wall Street Journal (WSJ), covering the period from January 1, 2018, to October 31, 2022. Python is utilized to scrape newspaper articles by day, then to combine all articles and filter the articles related to U.S trade.

The S&P 500 stock index data is scraped from the yahoo finance website utilizing the R package quantmod. The period covers January 1, 2018, and October 31, 2022.

# Platforms
R is utilized to scrape S&P 500 stock index data from the yahoo finance website.

Python is used to scrape newspaper articles from the Wall Street Journal website.

Python is the main platform for this project. Some Python packages, including numpy, pandas, matplotlib, seaborn, sys, cvs, string, statsmodels, scipy, nltk, sklearn, spicy, genism, pickle, vaderSentiment, and textblob, etc. are used to preprocess raw text data, including tokenization, removing stop and punctuation words, stemming and lemmatization, etc. and to do topic modeling, sentiment analysis, time-series analysis and machine learning model building.

# Data Analysis 
Code file for data analysis part could be found at [here](https://minshimia.github.io/Natural-Language-Processing/BUAN_6342_NLP_Project_Min_Shi.html) for more details, the analysis could be found at the [slides](https://minshimia.github.io/Natural-Language-Processing/BUAN_6342_NLP_Presentation_Min_Shi.pdf).

# Conclusion
Naïve Bayes model is the best model according to ROC AUC value and Random Forest model has the best performance according to testing score. Besides, there is no big difference on the model accuracy utilizing different vectorizers to generate the matrix of token counts.

We could try to use NLP analysis of WSJ newspaper articles related to U.S. trade to predict the changes of stock price.



