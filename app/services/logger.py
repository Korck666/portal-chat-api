import logging
from services.mongodb_handler import MongoDBHandler
from services.mongodb import collections, MDB_LOGS 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = MongoDBHandler(collection=collections[MDB_LOGS])

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(handler)
