"""
---
Airbnb_pkg -  This package has been created to contain all the functions to process the airbnb data 
---

Initial Cleaning Functions: 
|_ clean_calendar_data - Basic clean on the raw calender data
|_ clean_listings_data - Basic clean on the raw listings data
|_ clean_reviews_data  - Basic clean on the raw reviews data
|_ data_merge - Merges the calender & listing data on 'id'
|_ ML_preprocessing - Creates the imput for the machine learning process

---
"""
## Imports

import pandas as pd
import numpy as np

# Sklearn for data prep
from sklearn.preprocessing import MultiLabelBinarizer
import re

## Initial Cleaning Functions

def clean_calendar_data(data):
    """
    This fuction is to perform a basic clean on the raw calender data.
    """
    # The price is only useful for days that have data so drop NaN's in this case
    # We can interpolate these days in for the seasonal analysis    
    data = data.dropna()

    # Update the formatting of the prices to be an integer    
    data['price'] = [int(str(x).replace('$','').replace(',','').replace('.00','')) 
                     for x in data['price']] 
    
    # Sets Date column as datetime
    data['date'] = pd.to_datetime(data['date'])

    # Drops unwanted columns (Just the )
    data = data[['listing_id','price','date']]
    
    return data
    
def clean_listings_data(data):
    """
    This fuction is to perform a basic clean the raw listings data.
    """
    # Keep only columns that may influence cost including property size, neighbourhood, price & reviews
    # Dropped columns including state, dates of reviews, availability, if it's bookable, host info
    # All dropped columns should have very little to do with how much the AirBnB costs
    # Variables like steert were seen as being to granular    
    keep_col = ['id', 'neighbourhood', 'zipcode', 'property_type', 
                'room_type', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 
                'bed_type', 'amenities', 'square_feet', 'price', 'weekly_price', 
                'monthly_price', 'number_of_reviews', 'review_scores_rating',
                'review_scores_accuracy', 'review_scores_cleanliness', 
                'review_scores_checkin', 'review_scores_communication', 
                'review_scores_location', 'review_scores_value', 'reviews_per_month']

    data = data[keep_col]

    # Removes and prints columns with more than 90% of data missing
    # Just drops 'square_feet' as it has very little data
    data_dpcol = data.dropna(axis=1, thresh=len(data)*0.1)
    dropped_col = set(data.columns).difference(list(data_dpcol.columns))
    print(f'Columns dropped: {dropped_col}')
    
    # Removes rows with all missing values (Othes may be useful)
    data_fil = data_dpcol.dropna(axis=0, thresh=1)
    print(f'Number of rows dropped: {len(data_dpcol)-len(data_fil)}')

    # Selects the columns related to price
    price_columns = ['price','weekly_price','monthly_price']

    for column in price_columns:
        # Zero NaN's for now as they can be replaced by an average later on
        data_fil[column] = data_fil[column].fillna(0)

        # Formats the price columns
        data_fil[column] = [int(str(x).replace('$','').replace(',','').replace('.00','')) 
                            for x in data_fil[column]]

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

def data_merge(calendar_data, listings_data):
    """
    This function merges the two most useful datasets for this analysis calender & listings
    """
    # Group the data by listing
    calendar_data = calendar_data.groupby('listing_id').median().round()
    
    # Set the listing_id as the index and drop date for calendar_data
    calendar_data = calendar_data[['price']]
    calendar_data.columns = ['Cal_price']
    
    # Set the index for Listings as id
    listings_data.index = listings_data['id']
    listings_data = listings_data.drop(columns=['id'])
    
    # For the sake of this analysis  
    merged_data = pd.merge(calendar_data, listings_data, left_index=True, right_index=True)
    
    return merged_data

def ML_preprocessing(calendar_data, listings_data):
    """
    This function has been created to prep the data ready for ML
    """
    
    # Run the basic cleaning functions  
    cal_cleaned = clean_calendar_data(calendar_data)
    list_cleaned = clean_listings_data(listings_data)
    
    # Merge the two datasets
    data_merged = data_merge(cal_cleaned, list_cleaned)
    
    # Drop all unwanted columns    
    data_drop = data_merged.drop(columns=['price','weekly_price','monthly_price','neighbourhood'])
    
    # Replace NaN's in Numerical Catagorical Variables with mode
    numeric_cata = ['review_scores_rating','accommodates',
                    'bathrooms','bedrooms','beds',
                    'review_scores_accuracy','review_scores_cleanliness',
                    'review_scores_checkin','review_scores_communication',
                    'review_scores_location','review_scores_value']
    data_drop[numeric_cata] = data_drop[numeric_cata].fillna(data_drop.mode().iloc[0])
                                                               
    # Replace NaN's in reviews_per_month with the average rounded
    rev_col = ['reviews_per_month']
    data_drop[rev_col] = data_drop[rev_col].fillna(data_drop[rev_col].median().round())
    
    # Drop any other rows with NaN's (Should be minimal)     
    data_drop = data_drop.dropna()
    
    # Some processing needs to be used to edit bad zipcodes
    data_drop['zipcode'] = [re.sub(r'\b(\d{1,4}|\d{6,}|\D)\b','',x)[0:5] 
                            for x in data_drop['zipcode']]
    
    # Turn the amenities data into a list of amenities
    data_drop['amenities'] = [x.replace('{','').replace('}','').replace('"','').split(',') 
                                 for x in data_drop['amenities']]
    
    # One hot encode the 'amenities data'
    mlb = MultiLabelBinarizer()
    amenities = pd.DataFrame(mlb.fit_transform(data_drop.pop('amenities')),
                              columns=mlb.classes_,
                              index=data_drop.index)
    
    # Create dummies for all of the other catagorical columns
    non_numeric_cata = ['zipcode', 'property_type', 'room_type', 'bed_type']
    nn_cata = pd.get_dummies(data_drop[non_numeric_cata])
    
    # Merge the data frames & drop extra columns to create the ML Input
    data_temp = pd.merge(data_drop, nn_cata, left_index=True, right_index=True)
    data_output =  pd.merge(data_temp, amenities, left_index=True, right_index=True)
    data_output = data_output.drop(columns=['zipcode', 'property_type', 'room_type', 'bed_type',''])
    
    return data_output