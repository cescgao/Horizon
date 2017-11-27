# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Nov 2017

import logging

logger = logging.getLogger()

stream = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s[%(asctime)s %(module)s:%(lineno)d] %(message)s')
stream.setFormatter(formatter)
logger.addHandler(stream)
