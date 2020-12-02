#!/usr/bin/env python

"""
test code for pcats api client

can be run with py.test
"""

import os
from pathlib import Path

import pytest

import pcats_api_client
# from pcats_api_client import pcats_api

def test_pcats_api():
    pcats_api_client.job_status("098")
    # pcats_api.job_status("098")


