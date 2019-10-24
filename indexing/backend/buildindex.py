import json
from backend.InvertedIndex import InvertedIndex
from backend.JsonOps import JsonParser

inputFile="PlacesResults.json"
indexFile="PlacesIndex.json"
documentFile="PlacesDoc.json"

invIndex = InvertedIndex(inputFile, indexFile, documentFile)
invIndex.buildIndex()
