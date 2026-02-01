from pydantic import BaseModel
from typing import List

class FeaturesRequest(BaseModel):
    features: List[float]
