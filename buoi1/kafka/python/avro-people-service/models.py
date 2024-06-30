from pydantic import BaseModel
from typing import Optional
import logging

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO
)

class Person(BaseModel):
    first_name : Optional[str]
    last_name : Optional[str]
    title : str
    
class SuccessHandler:
    def __init__(self, person) -> None:
        self.person = person
        
    def __call__(self, *args, **kwargs):
        err = args[0]
        msg = args[1]
        
        if err is not None:
            logger.error(f"Message delivery failed for person {self.person}: {err}")
            
        else:
            logger.info(f"""
                        Successfully produced:
                            - person: {self.person}
                            - topic: {msg.topic()}
                            - partition: {msg.partition()}
                            - offset: {msg.offset()}
                        """)