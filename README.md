# soh_data_extract
Tool for extracting data from SOH using WooCommerce API 

To use the tool, create a config.ini file copy the following lines to the file.
Replace the <> tag with your value

; config.ini
[DEFAULT]
HOST=<Host>
APP_NAME =Extract data
USER_ID=<user id>
CONSUMER_KEY=<consumer_key>
CONSUMER_SECERT=<consumer_secert>

Then Exectue the soh_online.py script to start extracting data from SOH. There will be 2 csv files generated, 
they are order_products.csv & orders.csv.
