from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

from ..schemes import PaginationScheme


class ReviewProductScheme(BaseModel):
    product_id: Annotated[int, Query(gt=0)]
    new: Annotated[bool, Query(default=False)]
    more_likes: Annotated[bool, Query(default=False)]
    pagination: Annotated[PaginationScheme, Depends()]


ReviewsProductDep = Annotated[ReviewProductScheme, Depends()]
