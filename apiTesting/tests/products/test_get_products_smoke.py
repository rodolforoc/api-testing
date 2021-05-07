import pytest
from apiTesting.src.utilities.requestsUtility import RequestsUtility
from apiTesting.src.dao.products_dao import ProductsDAO
from apiTesting.src.helpers.products_helper import ProductsHelper

pytestmark = [pytest.mark.products, pytest.mark.smoke]

@pytest.mark.tcid24
def test_get_all_products():
    req_helper = RequestsUtility()
    rs_api = req_helper.get(endpoint='products')

    assert rs_api, f"Get all products endpoint returned nothing"

@pytest.mark.tcid25
def test_get_product_by_id():

    # get a product from DB
    random_product = ProductsDAO().get_random_product_from_db(1)
    random_product_id = random_product[0]['ID']
    db_product_name = random_product[0]['post_title']

    # make the call
    product_helper = ProductsHelper()
    rs_api = product_helper.get_product_by_id(random_product_id)
    api_product_name = rs_api['name']

    # verify the response
    assert db_product_name == api_product_name, f"Get product by id returned wrong product. Id: {random_product_id}" \
                                                f"DB Name: {db_product_name}, API Name: {api_product_name}."