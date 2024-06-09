from pydantic import BaseModel
import logging

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO
)

class Person(BaseModel):
    id : str
    name : str
    title : str
    company : str
    YOE : int
    
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