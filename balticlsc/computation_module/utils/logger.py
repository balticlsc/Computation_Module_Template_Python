import logging
logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s (%(filename)s:%(lineno)d)',
    datefmt='%Y-%m-%d:%H:%M:%S')
logger = logging.getLogger('api')
