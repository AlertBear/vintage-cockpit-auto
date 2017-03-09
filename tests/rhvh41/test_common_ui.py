import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.rhvh41.node_status_page import NodeStatusPage

from fabric.api import env, run
from conf import *