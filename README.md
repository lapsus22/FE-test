# FE-test

To execute the main script, its necesary to use python main.py

The Jupyter notebook is used as a developing and debuging tool

I used the following libraries in the script: Pandas, Numpy and PDFPlumber

## Challenge

The main challenge I faced in this data extraction was the lack of consistency of the PDF extraction library with the document tables, since most of them werent fully encased in edges and workarounds were needed. At the end a solution was found and is working solidly.

## Approach

My main aproach was to extract the data as clean-ly as possible, once the data was in a format that was easy to manipulate I did a first clean-up while in list form to then build the Pandas DataFrame.
Once it was built the main objective was to convert all the relevant columns into float type objects to make the data easy to work in the future.