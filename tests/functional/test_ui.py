#!/usr/bin/env python3

import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_redirect(selenium):
    selenium.get('https://cloud.redhat.com/openshift')
    assert selenium.current_url.split('?')[0] == \
        'https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/auth'  # noqa


def test_title(selenium):
    selenium.get('https://cloud.redhat.com/openshift')
    assert selenium.title == 'Log in to Red Hat IDP'


def test_successful_login(selenium):
    selenium.get('https://cloud.redhat.com/openshift')
    selenium.find_element_by_id('username').send_keys(os.environ['username'])
    selenium.find_element_by_id('password').send_keys(os.environ['password'])
    selenium.find_element_by_id('_eventId_submit').click()
    try:
        WebDriverWait(selenium, 10).until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "pf-c-dropdown__toggle-text"),
                "{0}".format(os.environ['displayname'])))
    except Exception:
        return False
