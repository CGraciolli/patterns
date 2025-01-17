from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int
    
    
    def choose_batch(self, batch1, batch2):
                
        ## really should be an Enumarate
        if batch1.can_allocate(self) and batch2.can_allocate(self):
            if batch1.batch_type == batch2.batch_type:
                if batch1.eta <= batch2.eta:
                    return batch1
                else:
                    return batch2
            elif batch1.batch_type == "warehouse":
                return batch1
            else:
                return batch2
        elif batch1.can_allocate(self):
            return batch1
        elif batch2.can_allocate(self):
            return batch2
        else:
            return None


 ## TODO: shipment and warehouse shoul be an Enumerate
class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date] = None, batch_type: str = None):
        self.reference = ref
        self.sku = sku
        self.qty = qty
        self.eta = eta
        self.batch_type = batch_type
        self.available_qty = qty
    
    
    def can_allocate(self, order: OrderLine) -> bool:
        if self.sku == order.sku:
            return self.available_qty >= order.qty
        else:
            return False
    
    def allocate(self, order: OrderLine) -> None:
        if self.can_allocate(order):
            self.available_qty -= order.qty
