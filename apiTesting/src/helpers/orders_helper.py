from apiTesting.src.utilities.wooAPIUtility import WooAPIUtility
from apiTesting.src.dao.orders_dao import OrdersDAO
import json
import os

class OrdersHelper(object):

    def __init__(self):
        self.cur_file_dir = os.path.dirname((os.path.realpath(__file__)))
        self.woo_helper = WooAPIUtility()

    def create_order(self, additonal_args=None):

        payload_template = os.path.join(self.cur_file_dir, '..', 'data', 'create_order_payload.json')

        with open(payload_template) as f:
            payload = json.load(f)

        # if user adds more info to payload, then update it
        if additonal_args:
            assert isinstance(additonal_args, dict), f"Parameter 'additional_args' must be a dictionary" \
                                                     f"but found {type(additonal_args)}"
            payload.update(additonal_args)

        rs_api = self.woo_helper.post('orders', params=payload, expected_status_code=201)

        return rs_api

    @staticmethod
    def verify_order_is_created(order_json, expected_cust_id, expected_products):
        orders_dao = OrdersDAO()

        # verify the response
        assert order_json, F"Create orde response is empty"
        assert order_json['customer_id'] == expected_cust_id, f"Create order with given customer id returned" \
                                                         f"bad customer id. Expected customer_id={expected_cust_id} but got '{order_json['customer_id']}"
        assert len(order_json['line_items']) == len(expected_products), f"Expected only {len(expected_products)} item in order but " \
                                                           f"found {len(order_json['line_items'])}" \
                                                           f"Order: {order_json['id']}"

        # verify in db
        order_id = order_json['id']
        line_info = orders_dao.get_order_lines_by_order(order_id)
        assert line_info, f"Create order, line item not found in DB. Order id: {order_id}"

        line_items = [i for i in line_info if i['order_item_type'] == 'line_item']
        assert len(line_items) == 1, f"Expected 1 line but found {len(line_items)}. Order id: {order_id}"

        # get list of product ids in the response
        api_product_ids = [i['product_id'] for i in order_json['line_items']]

        for product in expected_products:
            assert product['product_id'] in api_product_ids, f"Create order does not have at least 1 expected product in DB." \
                                                             f"Product id: {product['product_id']}. Order: {order_id}"
