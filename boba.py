#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 16:16:28 2023

@author: gs
"""

import pandas as pd
from yelpapi import YelpAPI
import os

api_key = api_key

try:
    yelp_api = YelpAPI(api_key)

    # Create an empty list to store boba shop data
    boba_shops = []

    # Define the total number of entries you want to fetch
    total_entries = 200

    # Yelp API has a limit of 50 results per request
    limit_per_request = 50

    # Number of requests needed to reach the desired total_entries
    num_requests = (total_entries + limit_per_request - 1) // limit_per_request

    for request_num in range(num_requests):
        # Calculate the offset for the current request2
        offset = request_num * limit_per_request

        # Make the API request with the current location, term, radius, limit, and offset
        search_results = yelp_api.search_query(
            location="Raleigh, NC", term="bubble tea", radius=40000, limit=limit_per_request, offset=offset
        )

        for bus in search_results["businesses"]:
            business_id = bus.get("id")
            if business_id and not any(b.get("id") == business_id for b in boba_shops):
                # Check if "Bubble Tea" is in the Categories field
                business_categories = [cat["title"] for cat in bus["categories"]]
                if "Bubble Tea" in business_categories:
                    reviews = yelp_api.reviews_query(id=business_id)
                    review_texts = [review["text"] for review in reviews["reviews"]]

                    boba_shop_data = {
                        "Name": bus["name"],
                        "Phone": bus.get("phone", ""),
                        "Rating": bus.get("rating", ""),
                        "Address": ", ".join(bus["location"]["display_address"]),
                        "Street Address": bus["location"]["display_address"][0],
                        "City": list(bus["location"].values())[3],
                        "Categories": ", ".join(business_categories),
                        "Review Count": bus.get("review_count", ""),
                        "Latitude": bus["coordinates"]["latitude"],
                        "Longitude": bus["coordinates"]["longitude"],
                        "Reviews": review_texts
                    }

                    boba_shops.append(boba_shop_data)

    # Create a DataFrame from the list of boba shop data
    df = pd.DataFrame(boba_shops)

    # Save the DataFrame to a CSV file
    downloads_folder = os.path.expanduser("~/Downloads")
    file_path = os.path.join(downloads_folder, "rdu_boba_shops.csv")
    df.to_csv(file_path, index=False)

finally:
    yelp_api.close()

print("Data saved to rdu_boba_shops.csv")
#%%
# Define a list of stores and their addresses
stores = [
    {"name":"Grand Asia Market","address": "1253 Buck Jones Rd, Raleigh, NC 27606"},
    {"name": "Bumble Tea", "address": "3221 Avent Ferry Rd, Raleigh, NC 27606"},
    {"name": "Tea Hill", "address": " 318 W Franklin St, Chapel Hill, NC 27516"}
    ]

# Create empty lists to store data for all stores
all_store_data = []

try:
    yelp_api = YelpAPI(api_key)

    for store_data in stores:
        store_name = store_data["name"]
        store_address = store_data["address"]

        # Search for the specific store using its name and address
        search_results = yelp_api.search_query(location="Raleigh, NC", term=store_name, limit=1)

        # Check if the store was found in the search results
        if "businesses" in search_results and len(search_results["businesses"]) > 0:
            store_info = search_results["businesses"][0]
            store_id = store_info["id"]

            # Fetch the reviews for the specific store
            reviews = yelp_api.reviews_query(id=store_id)
            review_texts = [review["text"] for review in reviews["reviews"]]

            # Extract the latitude and longitude
            latitude = store_info["coordinates"]["latitude"]
            longitude = store_info["coordinates"]["longitude"]

            # Create a dictionary with the store information
            store_data = {
                "Store Name": store_info["name"],
                "Store Address": ", ".join(store_info["location"]["display_address"]),
                "Latitude": latitude,
                "Longitude": longitude,
                "Reviews": review_texts
            }

            all_store_data.append(store_data)

    # Create a DataFrame with all the store data
    df = pd.DataFrame(all_store_data)

    # Save the DataFrame to a single CSV file
    csv_file = "all_stores_info.csv"
    df.to_csv(csv_file, index=False)

    print(f"Store information for all stores saved to {csv_file}")

finally:
    yelp_api.close()

