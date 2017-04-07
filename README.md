# Textmining
Stemming and creation of vector representation of documents to search efficiently

The objective of this project is to make flat file documents more searchable. First procedure is to remove the filler words and stem the words using porter stemmer algorithm. 

The search and stemming is performed using python and a REST service is created using Flask framework to perform the above said tasks. 

Inverse-document-frequency, precision and recall are calculated to support the efficiency of the search performed.

A simple front end is created using asp .net which receives the search result in JSON format from the RESTApi.
