# stdlib
import time

# 3rd party
import pytest

# local
from . import DRIVER, SITE_URL


class TestStaticContent(object):
    @classmethod
    def setup_class(self):
        self.driver = DRIVER()
        self.driver.set_window_size(1600, 1200)

    @classmethod
    def teardown_class(self):
        self.driver.close()

    @pytest.fixture
    def site(self):
        self.driver.get(SITE_URL)

    def test_pageload(self, site):
        assert self.driver.title == 'Boulder Python'

    def test_maintainers(self, site):
        organizers = self.driver.find_element_by_xpath("/html[@class='dark fa-events-icons-ready']/body/div[@class='body-content']/div[@class='content']/div[@class='section-body'][3]")
        assert 'Scott Vitale' in organizers.text
        assert 'Zoë Farmer' in organizers.text
        assert 'Frank Valcarcel' in organizers.text

    def test_privacy(self):
        self.driver.get(f'{SITE_URL}/privacy')

        header = self.driver.find_element_by_xpath("/html[@class='dark fa-events-icons-ready']/body/div[@class='body-content']/h1")
        assert header.text == 'Privacy Notice'
