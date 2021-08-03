# Introduction
This is the 2nd project for the Python path of Openclassrooms. The goal is to web scrape from [Books to Scrape](http://books.toscrape.com/)
and to extract the following things:
1. All categories
2. All products (books) in each category
3. All required details for each product

Then it takes all the above and saves it all in separate lists within a CSV file (1 file for each category).

It also saves the image from each product and organizes them by the book's category, in a separate folder, with the name of
the book it belongs to.


# Required Setup to run the program:

1. Create the directory in which you want to keep the program.
2. Open your terminal.
3. Navigate to the folder with the main.py and requirements.txt
4. Create your Virtual Environment by running the command: `python -m venv .venv`
5. Activate the Environment by running: `.venv\Scripts\activate.bat` (Windows) or `source .venv/bin/activate` (OS)
6. Install the Requirements by running the command: `pip install -r requirements.txt`
   
# How to run the program:
1. Open your terminal
2. Navigate to the directory which contains the >main.py< file
3. Activate the Environment by running: `.venv\Scripts\activate.bat` (Windows) or `source .venv/bin/activate` (OS)
4. Run the command: `python main.py`
5. While the program runs, it will continuously display the current category and the last title of each book it 
   successfully saved.
   
## Notes
- The program will create all files and folders automatically in the program directory.

## Technologies
- Python version 3.9.5

- Beautifulsoup4 version 4.9.3

- Requests version 2.6.0
