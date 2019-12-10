from bs4 import BeautifulSoup
import json
import io

# Pages to parse
pages = [
     "./pages/(4) Budget Tips - USA, For Aussie Travellers.htm",
     "./pages/Las Vegas For Aussie Travellers.htm"
     "./pages/CALIFORNIA USA Backpacker _ Traveler.htm"
     "./pages/Florida Travel For Less.htm"
     "./pages/FLORIDA USA Backpacker _ Traveler.htm"
     "./pages/Glacier National Park.htm"
     "./pages/New York City Travel Tips.htm"
     "./pages/Travelling USA.htm"
     "./pages/What to do in New York_.htm"
     "./pages/TRAVEL GEORGIA..html"
     "./pages/NEW YORK CITY USA Backpacker _ Traveler.htm"
     "./pages/Travelers of the U.S. National Parks.html"
     "./pages/San Francisco Family Travel + Activities.htm"
]

#Array of found places to output
places = []

for page in pages:
     soup = BeautifulSoup(open(page), "html.parser")

     for i, place in enumerate(soup.find_all('div', {'class': '_2pie _5_ts'})):
          title = place.find("a", {'class' : '_r-g'}, recursive=True)
          address = place.find("div", {'class' : '_r-k'}, recursive=True)

          titleString = "".join([str(x) for x in title.contents]) 

          if address is not None: 
               addressString = "".join([str(x) for x in address.contents]) 
          else: 
               addressString = ""

          places.append({"name": titleString, "address": addressString})

y = json.dumps(places, ensure_ascii=False).encode('utf8')
print(len(places))
print(y.decode())
