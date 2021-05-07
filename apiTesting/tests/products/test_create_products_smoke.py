import json

from apiTesting.src.utilities.genericUtilities import generate_random_string
from apiTesting.src.helpers.products_helper import ProductsHelper
from apiTesting.src.dao.products_dao import ProductsDAO
import pytest

pytestmark = [pytest.mark.products, pytest.mark.smoke]

@pytest.mark.tcid26
def test_create_1_simple_product():

    # generate some data
    payload = dict()
    payload['name'] = generate_random_string()
    payload['type'] = "simple"
    payload['regular_price'] = "10.99"

    # make a call
    products_rs = ProductsHelper().call_create_product(payload=json.dumps(payload))

    # Verify the response is not empty
    assert products_rs, f"Create product API response is empty. Payload: {payload}"
    assert products_rs['name'] == payload['name'], f"Create product call response has" \
           f"unexpected name. Expected: {payload['name']}, Actual: {products_rs['name']}"

    # verify the product exists in DB
    product_id = products_rs['id']
    db_product = ProductsDAO().get_product_by_id(product_id=product_id)

    assert payload['name'] == db_product[0]['post_title'], f"Create product, title in db does not match" \
            f"title in api. DB: {db_product[0]['post_title']}. API: {payload['name']}"