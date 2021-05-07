import pytest
import logging as logger

from apiTesting.src.utilities.genericUtilities import generate_random_email_and_password

@pytest.mark.tcid29
def test_create_customer_only_email_password():

    logger.info("TEST: Create new customer with email and password only")
    rand_info = generate_random_email_and_password()
    logger.info(rand_info)
    email = ''
    password = ''

    # create payload


    # make the call


    # verify status code of the call

    # verify the email in the response

    # verify customer is created in database