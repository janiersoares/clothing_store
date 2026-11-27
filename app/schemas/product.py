from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, model_validator

Gender = Literal["masculino", "feminino"]
ProductType = Literal["roupa", "calcado"]
Season = Literal["inverno", "verao"]

CLOTHING_SIZES = {"P", "M", "G", "GG"}
SHOE_SIZES = {str(number) for number in range(33, 46)}


class VariantIn(BaseModel):
    size: str
    stock: int = Field(ge=0)


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    price: Decimal = Field(ge=0)
    discount: Decimal | None = Field(default=None, ge=0)
    photo_url: str | None = None
    gender: Gender
    product_type: ProductType
    season: Season | None = None
    variants: list[VariantIn] = Field(min_length=1)

    @model_validator(mode="after")
    def check_product_rules(self) -> "ProductCreate":
        if self.discount is not None and self.discount > self.price:
            raise ValueError("discount cannot be greater than price")

        if self.product_type == "roupa":
            if self.season is None:
                raise ValueError("clothing requires a season")
            allowed_sizes = CLOTHING_SIZES
        else:
            if self.season is not None:
                raise ValueError("shoes cannot have a season")
            allowed_sizes = SHOE_SIZES

        sizes = [variant.size for variant in self.variants]
        if len(sizes) != len(set(sizes)):
            raise ValueError("each size can appear only once")

        invalid_sizes = set(sizes) - allowed_sizes
        if invalid_sizes:
            raise ValueError(f"invalid sizes for {self.product_type}: {sorted(invalid_sizes)}")

        return self