import json

import pytest
import logging as logger

from apiTesting.src.utilities.genericUtilities import generate_random_email_and_password
from apiTesting.src.helpers.customers_helper import CustomerHelper
from apiTesting.src.dao.customers_dao import CustomersDAO
from apiTesting.src.utilities.requestsUtility import RequestsUtility

@pytest.mark.tcid29
@pytest.mark.customers
def test_create_customer_only_email_password():

    logger.info("TEST: Create new customer with email and password only")
    rand_info = generate_random_email_and_password()
    email = rand_info['email']
    password = rand_info['password']

    # make the call
    cust_obj = CustomerHelper()
    cust_api_info = cust_obj.create_customer(email=email, password=password)

    # verify the email in the response
    assert cust_api_info['email'] == email, f"Create customer api return wrong email. Email: {email}"
    assert cust_api_info['first_name'] == '', f"Create customer api returned value for first_name" \
                                              f"but it should be empty"

    # verify customer is created in database
    cust_dao = CustomersDAO()
    cust_info = cust_dao.get_customer_by_email(email)

    id_in_api = cust_api_info['id']
    id_in_db = cust_info[0]['ID']

    assert id_in_db == id_in_api, f"Create customer response 'id' not same as 'ID' in database." \
                                  f"Email: {email}"


@pytest.mark.tcid47
@pytest.mark.customers
def test_create_customer_fail_for_existing_email():

    # get existing email from DB
    cust_dao = CustomersDAO()
    existing_cust = cust_dao.get_random_customer_from_db()
    existing_email = existing_cust[0]['user_email']

    # call the api
    req_helper = RequestsUtility()

    payload = {"email": existing_email, "password": "Password1"}

    cust_api_info = req_helper.post(endpoint='customers', payload=json.dumps(payload), expected_status_code=400)

    assert cust_api_info['code'] == 'registration-error-email-exists', f"Create customer with" \
           f"existing user error 'code' is not correct. Expected: 'registrations-error-email-exists'," \
           f"Actual: {cust_api_info['code']}"

    assert cust_api_info['message'] == 'An account is already registered with your email address. <a href="#" class="showlogin">Please log in.</a>', f"Create customer with" \
           f"existing user error 'message' is not correct. Expected: 'An account is already registered with your email address. <a href=\"#\" class=\"showlogin\">Please log in.</a>'," \
           f"Actual: {cust_api_info['message']}"
