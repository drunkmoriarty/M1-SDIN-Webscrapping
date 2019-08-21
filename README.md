# M1-SDIN-Webscrapping
This project was a homework for Python class. 

The goal of this program is to scrapp two e-commerce website to gather data such as the name of product, the price and the category where it belongs. The collected data is then used to compare the two website and to create a predictive model for the price of a product which is common to both websites. 

The program has a lot of flaws : 
- It has been built for two websites in particular (Redbubble and CafePress). 
- The structure of both sites cannot provide a deep gathering of the data around the product (My goal was to use the model category in order to include it as a variable in the linear regression). 

Important : the HTML code of both website changes from time to time. This implies that the expression pattern used in this code (through regular expression package) is out of date.
