# Introduction
This is the 2nd project for the Python path of Openclassrooms. The goal is to web scrape from [Books to Scrape](http://books.toscrape.com/)
and to extract the following things:
1. ALL Categories
2. All products (books) in each category
3. All required details for each product

Then it takes all the above and saves it all in separate lists within a CSV file (1 file for each category).

It also saves the image from each product in a separate folder and organizes them by the book's category with the name of
the book it belongs to.


# Required Setup to run the Program:

1. Open your terminal.
2. Navigate to the folder with requirements.txt
3. run the following command: `pip install -r requirements.txt`
   
# How to run the program:
1. Open your terminal
2. Navigate to the directory which contains the >main.py< file
3. run the command: `python main.py`
4. while running the Program will continuously display the current category, and the last title of each book it 
   successfully saved.
## Notes
- The program will create all files and folders automatically in the same program directory.

## Technologies
- Python version 3.9.5

- Beautifulsoup4 version 4.9.3

- Requests version 2.6.0
