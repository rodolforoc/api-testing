from apiTesting.src.helpers.orders_helper import OrdersHelper
from apiTesting.src.utilities.wooAPIUtility import WooAPIUtility
from apiTesting.src.utilities.genericUtilities import generate_random_string
import pytest


pytestmark = [pytest.mark.orders, pytest.mark.regression]

@pytest.mark.parametrize("new_status", [
    pytest.param('cancelled', marks=pytest.mark.tcid55),
    pytest.param('completed', marks=pytest.mark.tcid56),
    pytest.param('on-hold', marks=pytest.mark.tcid57)
])
def test_update_order_status(new_status):
    order_helper = OrdersHelper()
    # create new order
    order_json = order_helper.create_order()
    cur_status = order_json['status']

    assert cur_status != new_status, f"Current status of order is already {new_status}." \
                                     f"Unable to run test."

    # update the status
    order_id = order_json['id']
    payload = {"status": new_status}
    order_helper.call_update_order(order_id=order_id, payload=payload)

    # get order information
    new_order_info = order_helper.call_retrieve_an_order(order_id)

    # verify the new order status is updated
    assert new_order_info['status'] == new_status, f"Updated order status to '{new_status}'," \
                                                   f"but order is still '{new_order_info['status']}'"

@pytest.mark.tcid58
def test_update_order_status_to_random_string():
    new_status = 'abdsad'
    order_helper = OrdersHelper()

    # create new order
    order_json = order_helper.create_order()
    order_id = order_json['id']

    # update the status
    payload = {"status": new_status}
    rs_api = WooAPIUtility().put(f'orders/{order_id}', params=payload, expected_status_code=400)

    assert rs_api['code'] == 'rest_invalid_param', f"Update order status to random string did no have " \
                                                   f"correct code in response. Expected: 'rest_invalid_param'" \
                                                   f"Actual: {rs_api['code']}."
    assert rs_api['message'] == 'Invalid parameter(s): status', f"Update order status to random string did no have " \
                                               f"correct message in response. Expected: 'Invalid parameter(s): status'" \
                                               f"Actual: {rs_api['message']}."

@pytest.mark.tcid59
def test_update_order_customer_note():
    order_helper = OrdersHelper()

    # create new order
    order_json = order_helper.create_order()
    order_id = order_json['id']

    random_string = generate_random_string(30)
    # update order
    payload = {"customer_note": random_string}
    order_helper.call_update_order(order_id=order_id, payload=payload)

    # get order information
    new_order_info = order_helper.call_retrieve_an_order(order_id)
    assert new_order_info['customer_note'] == random_string, f"Update order's 'customer_note' field" \
                                     f"failed. Expected: {random_string}. Actual: {new_order_info['customer_note']}"