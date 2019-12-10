# Dataset Creation
Places Insight's dataset was created by scraping places recommendations made on various Facebook travel groups.  The scraped names were then used to query Google Places API, the results of which were then compiled to create the dataset.

### PageParse.py
PageParse.py is a script that scrapes the Facebook pages for the names and addresses of place recommendations.  The scraped data is the sent to standard output, which can then be piped into a desired file.

### APICaller
Google Place API only allows calls from authenicated sites (meaning a site with a SSL/TLS certificate from a recognized CA).  To address this, APICaller can be opened in a site such as JSFiddle, which has the proper certificate.  APICalled can read in the output from PageParse.py which is used to query Google Place API.  Once all the querys have been run, the results can be downloaded as a JSON file.

### DataCleanser.py
Many of the Facebook groups how duplicate recommended places with one another.  DataCleanser iterates through the dataset created by APICalled and elimates duplicate places as well as aggregrates their unique reviews.