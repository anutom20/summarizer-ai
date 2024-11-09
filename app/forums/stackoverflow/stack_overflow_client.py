from stackapi import StackAPI
from app.config import STACKEXCHANGE_API_KEY
stackoverflow_client = StackAPI('stackoverflow', key=STACKEXCHANGE_API_KEY)
