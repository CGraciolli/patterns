from dataclasses import dataclass
from typing import Optional, List
from datetime import date


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self,
                 ref: str,
                 sku: str,
                 qty: int,
                 eta: Optional[date] = None):
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
    
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta    
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


def allocate(order: OrderLine, batches: List[Batch]) -> str | None:
    """Is given a OrderLine and a list of Batches,
    chooses the batch with the lowest eta to which the order can be allocated
    and returns its reference if possible,
    returns None if the other can't be allocated to aby of the batches.

    Args:
        order (OrderLine)
        batches (List[Batch])

    Returns:
        str: chosen batch reference
    """
    # first we filter the batches that can allocate
    allocatable_batches = list(filter(lambda batch: batch.can_allocate(order), batches))
    # then we choose the one with the smallest eta (None if possible)
    if len(allocatable_batches) > 0:
        chosen_batch = sorted(allocatable_batches)[0]
        # and we allocate the order to it
        chosen_batch.allocate(order)
        return chosen_batch.reference
    return None
