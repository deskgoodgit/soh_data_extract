import requests
import csv

class SOH_Online():

    def __init__(self, **kwargs):
        self.consumer_key = kwargs.get("consumer_key")
        self.consumer_secret = kwargs.get("consumer_secret")
        self.app_name = kwargs.get("app_name")
        self.host = kwargs.get("host")
        self.user_id = kwargs.get("user_id")
        #self._get_access_token()

    def get_all_orders(self):
        endpoint = "{}/{}".format(self.host, "/wc-api/v2/orders")
        params = {
            "consumer_key" : self.consumer_key,
            "consumer_secret" : self.consumer_secret,
            "page" : 1
        }
        columns = self._get_orders_columns()
        item_columns = self._get_item_columns()
        self._append_to_csv("orders.csv", columns+["line_items"])
        self._append_to_csv("order_products.csv", columns+["line_items"]+item_columns+['meta1','meta2','meta3'])
        #self._append_to_csv("order_products.csv", item_columns+['meta1','meta2','meta3'])
        while True:
            response = requests.get( endpoint, params=params)
            orders = response.json()["orders"]
            if len(orders) == 0:
                break
            for order in orders:
                row = []
                for column in columns:
                    if '.' not in column:
                        row.append(order[column])
                    else:
                        row.append(order[column.split(".")[0]][column.split(".")[1]])
                row.append(len(order["line_items"]))
                self._append_to_csv("orders.csv", row)
                for line_item in order["line_items"]:
                    item_row = []
                    for item_column in item_columns:
                        item_row.append(line_item[item_column])
                    for i in range(3):
                        if i < len(line_item["meta"]):
                            item_row.append(line_item["meta"][i]["value"])    
                        else:
                            item_row.append("")    
                    self._append_to_csv("order_products.csv", row+item_row)
                for fee_line in order["fee_lines"]:
                    self._append_to_csv("order_products.csv", row+[
                        fee_line["id"],
                        fee_line["total"],
                        fee_line["total"], 
                        1,
                        fee_line["title"],
                        fee_line["id"], "", "",""
                    ])

            params["page"]  = params["page"] + 1

    def _get_item_columns(self):
        return ["id", "subtotal", "total", "quantity", "name", "product_id"]

    def _append_to_csv(self, filename, row):
        with open(filename, 'a+', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(row)
        
    def _get_orders_columns(self):
        columns = ["id", "order_number", "created_at", "status", "total", "total_line_items_quantity", "shipping_methods"]
        columns = columns + ["payment_details.method_title", "shipping_address.address_1", "shipping_address.address_2", "shipping_address.city"]
        columns = columns + ["shipping_address.state", "shipping_address.country", "billing_address.email", "billing_address.phone", "billing_address.first_name"]
        columns = columns + ["customer_ip"]
        return columns


    def main():
        from soh_online import SOH_Online
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        soh = SOH_Online(host=config['DEFAULT']['HOST'], 
            app_name=config['DEFAULT']['APP_NAME'],
            user_id=config['DEFAULT']['USER_ID'],
            consumer_key=config['DEFAULT']['CONSUMER_KEY'],
            consumer_secret =config['DEFAULT']['CONSUMER_SECERT'])
        soh.get_all_orders()
    if __name__ == "__main__":
        main()