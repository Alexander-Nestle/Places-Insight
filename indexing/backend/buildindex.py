from indexing.backend.InvertedIndex import InvertedIndex

inputFile="PlacesResults.json"
indexFile="PlacesIndex.json"
documentFile="PlacesDoc.json"

invIndex = InvertedIndex(inputFile, indexFile, documentFile)
invIndex.buildIndex()
