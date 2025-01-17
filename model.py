from dataclass import dataclass
from typing import Optional
from datetime import date


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.qty = qty
        self.available_qty = qty
    
    def can_allocate(self, order: OrderLine) -> bool:
        return self.available_qty >= order.qty
    
    def allocate(self, order: OrderLine) -> None:
        if self.can_allocate(order):
            self.available_qty -= order.qty
