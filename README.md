# rsc-scraper

# Usage

These instructions assume very little knowledge. Feel free to DM me (mitchy.#6281) if you need additional help.

1. Get Python. If you get it from somewhere other than the Microsoft store, you'll have to add it to your path. [Here's the Microsoft Store version.](https://www.microsoft.com/store/productId/9NJ46SX7X90P)

2. Download these scraper files using the button labelled "Code" or "Download" above. If you're unsure of which option to pick, select "Download ZIP" and unzip the file.

3. Create a .csv file in the same format as the 'players.csv'. That is, 3 columns (RSC ID, player name*, and tracker link) with column headers. While all 3 columns must be present, the first two columns do not need to be accurate - they can be filled with any nonsense, as long as the tracker links are correct.

4. Right click on 'scrape.ps1' and select 'Run with PowerShell'. When PowerShell opens, you may be prompted with an Execution Policy Change. Pressing 'Y' or 'A' will move you past this prompt.

5. Make some tea, go for a jog, meditate, whatever. Scraping takes a while.

6. When the utility is finished, the PowerShell window will close and the MMR data will be stored in a new file: 'mmr.csv'

\* - There are many special characters that will cause errors if present in this column. I don't have an exhaustive list of said characters, but, as a broad rule of thumb if you can't see a character on your keyboard, it should be removed from player names to make this utility function. 
