#frontend is done by ayush and backend is done by rohit
import os
import requests
import json
from dotenv import load_dotenv

# --- SETUP ---
# Fix: Call load_dotenv() to load the .env file
load_dotenv()

# Get the API key from the environment
API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"


# --- MAIN LOGIC FUNCTION ---
def fetch_news(category):
    """
    Fetches news from the NewsAPI for a given category.
    Returns a list of articles or a list containing an error message.
    """
    
    # Fix: All the logic below is now correctly indented INSIDE the function.

    # First, check if the API key was loaded successfully.
    if not API_KEY:
        return [{"title": "Configuration Error", "description": "API key not found. Make sure you have a .env file with NEWS_API_KEY set."}]

    # Construct the full URL for the API request.
    url = f"{BASE_URL}?country=us&category={category}&apiKey={API_KEY}"
    
    # Fix: Correctly structured try...except block
    try:
        # Make the GET request to the API.
        response = requests.get(url)
        
        # Check if the request was successful (HTTP status code 200).
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])
            
            # Fix: Initialize an empty list to store our clean articles.
            clean_articles = []
            
            # Fix: Added a 'for' loop to process every article from the API.
            for article in articles:
                clean_articles.append({
                    "title": article.get("title", "No Title Available"),
                    "description": article.get("description", "No Description Available.")
                })
            return clean_articles
        else:
            # If the request failed, return an error message.
            return [{"title": "API Error", "description": f"Failed to fetch news. Status code: {response.status_code}. Please check your API key."}]
            
    except requests.exceptions.RequestException as e:
        # If there was a network problem, return a connection error message.
        return [{"title": "Network Error", "description": "Could not connect to the news service. Please check your internet connection."}]


import tkinter as tk
from tkinter import scrolledtext


#---IMPORTANT---
# This line imports the function from rohit file 
# Both files must be in the same folde for this to work



    #---UI FUNCTIONS---

def display_articles(category, text_widgets):
    """  Fetches news for a category and displays it in the text widgets"""
    # Clear the existing 
    text_widgets.config(state=tk.NORMAL)
    text_widgets.delete('1.0', tk.END)

    # Fetch the articles usingthe backend function
    articles =fetch_news(category)
    
    #Display the new articles
    if not articles:
        text_widgets.insert(tk.END, "No articles found or an error occurred.")
    else:
        for article in articles:
            # Insert articles title with a bullet point
            text_widgets.insert(tk.END,f" {article['title']}\n")
            # Insert articles description with indentation
            text_widgets.insert(tk.END, F"   {article['description']}\n\n")
    # Make the text widgets read-only again after updating content
    text_widgets.config(state=tk.DISABLED)


#--- MAIN UI SETUP---

# Create the main application window 
window = tk.Tk()
window.title ("News Aggregator")
window.geometry("800x600") # Set initial window size 

# Create a fame to hold the category buttons
# pady adds vertical padding around the frame 
button_frame = tk.Frame(window, pady=10)
button_frame.pack() # Pack the button frame at the top

# Create a frame to hold the news display area
#padx and pady add horizontal and vertical padding 
news_frame = tk.Frame(window, padx=10, pady=10)
#Pack the news frame,allowing it to expand and fill available space 
news_frame.pack(expand=True, fill=tk.BOTH)

# Create a scrolled text widget for displaying news articles
news_display = scrolledtext.ScrolledText(
    news_frame,
    wrap=tk.WORD,          # Wrap lines at word boundaries
    state=tk.DISABLED,     # Start in read-only mode
    font=("Helvetica", 12)  # Set Font style and size
)
# Pack the news dispaly to expand and fill the newss_frame
news_display.pack(expand=True, fill=tk.BOTH)

# --- CATEGORY BUTTONS ---
# Define the list of news categories
categories = ["business", "entertainment", "health","science","sports","technology"]

# Create a buttton for each category
for category in categories:
    button = tk.Button(
        button_frame,
        text=category.title(), # Dispaly category name with first letter capitalized
        # Use lambda to pass the specific category to dispaly_articles when buttons is clicked
        command=lambda cat=category: display_articles(cat, news_display)
    )
    # Pack buttons horizontally from left to right with some padding
    button.pack(side=tk.LEFT , padx=5)

#--- INITIAL LOAD ---
# Load the diapaly "general" news whaen the application first starts
display_articles("general", news_display)

# Start The Tkinter event loop
# This keeps the windows open and responsive to user interactions
window.mainloop()
