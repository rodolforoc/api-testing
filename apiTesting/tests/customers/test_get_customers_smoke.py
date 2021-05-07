import pytest
import logging as logger
from apiTesting.src.utilities.requestsUtility import RequestsUtility

@pytest.mark.tcid30
def test_get_all_customer():
    req_helper = RequestsUtility()
    rs_api = req_helper.get('customers')

    assert rs_api, f"Response of list all customer is empty"