from dataclasses import dataclass
from typing import Optional, List
from datetime import date
from enum import Enum, auto


class BatchType(Enum):
    WAREHOUSE = auto()
    SHIPMENT = auto()



@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int 

    def choose_batch(self, batch1, batch2):
        if batch1.can_allocate(self) and batch2.can_allocate(self):
            if batch1.batch_type.value == batch2.batch_type.value:
                if batch1.eta <= batch2.eta:
                    return batch1
                else:
                    return batch2
            elif batch1.batch_type.value < batch2.batch_type.value:
                return batch1
            else:
                return batch2
        elif batch1.can_allocate(self):
            return batch1
        elif batch2.can_allocate(self):
            return batch2
        else:
            return None


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, batch_type: BatchType, eta: Optional[date] = None):
        self.reference = ref
        self.sku = sku
        self.qty = qty
        self.eta = eta
        self.batch_type = batch_type
        self._available_qty = qty
        self._allocated_lines = []
    
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
