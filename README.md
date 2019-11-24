# Airbnb Market Analysis

In this repository I will examine data provided by Airbnb on both the Boston and Seattle markets to gain insights into the bussiness. The objective is to use the CRISP-DM data framework to answer some specific bussines questions. The aim of my analysis will be to recommend users a listing price based on various factors (e.g. location, amenities or size). The business case for this is simple, users with better prices wouldn't undervalue their property resulting in lost revenue or overvalue them losing out on bookings. 

This project will follow the CRISP-DM Process a framework for running datascience projects. It follows the core steps listed below:
- Business Understanding
- Data Understanding
- Prepare Data
- Data Modeling
- Evaluate the Results

I will split the CRISP-DM process into the following notebooks in this project:
- Bussiness Understanding & Data Understanding - Initial_Data_Analysis (Data Understanding).ipynb
- Data Proccessing - Data_Processing (Prepare Data).ipynb
- Data Modeling & Evaluation - Data_Processing (Data Modeling).ipynb

After the initial buissness understanding step I have came up with bussiness questions to focus on throughout the rest of the project:

The three initial buissness questions are as follows:
1) Does the price vary the seasonally across both Airbnb markets?
2) Which Airbnb listing variables will have the biggest impact on price?
3) Can I predict prices based on the market, amenities and seasonality?

All cleaning and general functions used in multiple notebooks will be stored in the airbnb_pkg.

## The Results

1) Does the price vary the seasonally across both Airbnb markets?

Interestingly the seasonal trend for the two markets are much more similar than expected considering they are on opposite sides of the US. They both have relavitely low seasonality with only Feb diverting from the rest of the year massively. Seattle also shows a low Januray well below that of Boston. Better results could be achieved by looking at seasonality of price over multiple years but this is unavalible in this data. It would also be great to compare this to avaliblity of the properties to see if properties are lowering prices in months when avaliblity is higher. That is out of the scopre of this project at this point.

2) Which Airbnb listing variables will have the biggest impact on price?

The results of the  feature importance show that the reviews per month, number it accomodates, number of reviews and number of bedrooms are the important features that can be used most to predict the price of an Airbnb. In terms of impact on price this suggests that the latent feature of number of people who can stay at an Airbnb has the biggest influence. This makes sense are the more people a property can hold is probably very related to how much they can charge. Features such as reviews per month and number of reviews would probably show how popular a property is and therefore if a user can charge more. While these are useful for current users (maybe Airbnb could tell users with a certain amount of reviews that they could increase their listing by X amount) they are not very useful for predicting price and so to answer my second question it would be worth removing these for the final model.

3) Can I predict prices based on the market, amenities and seasonality?

On the whole, the model has predicted the general trend well except for outlier properties. These may have low bookings or have other reasons for why the price varies from the trend(quality of the Airbnb for instance). Overall the model predicts prices well enough to provide recommendations to users and so achieves the core business objective.

## Acknowledgements

All of the data in this project was provided through Airbnb on Kaggle and used in conjunction with my Udacity Data Scientist Nanodegree.
