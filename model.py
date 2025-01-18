from dataclasses import dataclass
from typing import Optional, List
from datetime import date



@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int 


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date] = None):
        self.reference = ref
        self.sku = sku
        self.qty = qty
        self.eta = eta
        self._available_qty = qty
        self._allocated_lines = []
        
    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference
    
    def __hash__(self):
        return hash(self.reference)
    
    @property
    def available_qty(self) -> int:
        return self._available_qty
    
    @property
    def allocated_quantity(self) -> int:
        return self.qty - self.available_qty
    
    @property
    def allocated_lines(self) -> List[OrderLine]:
        return self._allocated_lines
    
    def can_allocate(self, order: OrderLine) -> bool:
        if order in self.allocated_lines:
            return False
        if self.sku == order.sku:
            return self._available_qty >= order.qty
        else:
            return False
    
    def allocate(self, order: OrderLine) -> None:
        if self.can_allocate(order):
            self._available_qty -= order.qty
            self._allocated_lines.append(order)
            
    def can_deallocate(self, order: OrderLine) -> bool:
        return order in self._allocated_lines
    
    def deallocate(self, order: OrderLine) -> None:
        if self.can_deallocate(order):
            self._allocated_lines.remove(order)
            self._available_qty += order.qty


def allocate(order: OrderLine, batches: List[Batch]) -> None:
    # first we filter the batches that can allocate
    allocatable_batches = filter(lambda batch: batch.can_allocate(order),
                                 batches)
    # then we choose the one with the smallest eta (None if possible)
    chosen_batch = min(allocatable_batches,
                       key=lambda batch: batch.eta or date.min,
                       default=None)
    
    # and we allocate the order to it
    if chosen_batch:
        chosen_batch.allocate(order)
    
