"""
---
Airbnb_pkg -  This package has been created to contain all the functions to process the airbnb data 
---

Initial Cleaning Functions: 
|_ clean_calendar_data - Basic clean on the raw calender data
|_ clean_listings_data - Basic clean on the raw listings data
|_ clean_reviews_data  - Basic clean on the raw reviews data

---
"""
## Imports

import pandas as pd
import numpy as np

## Initial Cleaning Functions

def clean_calendar_data(data):
    """
    This fuction is to perform a basic clean on the raw calender data.
    """
    # The price is only useful for days that have data so drop NaN's in this case
    data = data.dropna()

    # Update the formatting of the prices to be an integer    
    data['price'] = [int(str(x).replace('$','').replace(',','').replace('.00','')) 
                     for x in data['price']] 
    
    # Sets Date column as datetime
    data['date'] = pd.to_datetime(data['date'])

    # Drops unwanted columns
    data = data[['listing_id','price','date']]
    
    return data
    
def clean_listings_data(data):
    """
    This fuction is to perform a basic clean the raw listings data.
    """
    # Keep only columns related to our 3 core questions including property size, price & reviews
    keep_col = ['id', 'property_type', 'room_type', 'accommodates', 
                 'bathrooms', 'bedrooms', 'beds', 'square_feet',
                 'price', 'weekly_price', 'monthly_price', 
                 'security_deposit','cleaning_fee', 'number_of_reviews',
                 'first_review', 'last_review', 'review_scores_rating', 
                 'review_scores_accuracy', 'review_scores_cleanliness',
                 'review_scores_checkin', 'review_scores_communication', 
                 'review_scores_location', 'review_scores_value', 
                 'reviews_per_month']

    data = data[keep_col]

    # Removes and prints columns with more than 90% of data missing
    data_dpcol = data.dropna(axis=1, thresh=len(data)*0.1)
    dropped_col = set(data.columns).difference(list(data_dpcol.columns))
    print(f'Columns dropped: {dropped_col}')
    
    # Removes rows with all missing values (Othes may be useful)
    data_fil = data_dpcol.dropna(axis=0, thresh=1)
    print(f'Number of rows dropped: {len(data_dpcol)-len(data_fil)}')

    # Selects the columns related to price
    price_columns = ['price','weekly_price','monthly_price','security_deposit','cleaning_fee']

    for column in price_columns:
        # Zero NaN's for now as they can be replaced by an average later on
        data_fil[column] = data_fil[column].fillna(0)

        # Formats the price columns
        data_fil[column] = [int(str(x).replace('$','').replace(',','').replace('.00','')) 
                            for x in data_fil[column]]

    # Sets Date columns as datetime
    date_columns = ['first_review','last_review']
    for column in date_columns:
        data_fil[column] = pd.to_datetime(data_fil[column])
        
    return data_fil
    
    
def clean_reviews_data(data):
    """
    This fuction is to perform a basic clean the raw reviews data. 
    It is possible this data will not be needed for the analysis at this stage.
    """
    # Drops unwanted columns
    data = data[['listing_id','id','date','reviewer_id','comments']] 
    
    # Remove any data without comments as they won't be useful
    data = data.dropna()
    
    return data