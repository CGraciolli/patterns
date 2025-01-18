from datetime import date, timedelta
import pytest

# from model import ...
from model import allocate, OrderLine, Batch, OutOfStock

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


##warehouse eta = None
def test_prefers_warehouse_batches_to_shipments():
    order = OrderLine("order1", "sku1", 2)
    batch1 = Batch("batch1", "sku1", 20)
    batch2 = Batch("batch2", "sku1", 20, tomorrow)
    
    allocate(order, [batch1, batch2])
    
    assert batch1.available_qty == 18


def test_prefers_earlier_batches():
    order = OrderLine("order1", "sku1", 2)
    batch1 = Batch("batch1", "sku1", 20, tomorrow)
    batch2 = Batch("batch2", "sku1", 20, later)
    
    allocate(order, [batch1, batch2])
    
    assert batch1.available_qty == 18
    
    
def test_doesnt_choose_unallocatable_batches():
    order = OrderLine("order1", "sku1", 2)
    batch1 = Batch("batch1", "sku2", 20, tomorrow)
    batch2 = Batch("batch1", "sku1", 20, later)
    
    allocate(order, [batch1, batch2])
    
    assert batch2.available_qty == 18
    

def test_returns_allocated_batch_ref():
    order = OrderLine("order1", "sku1", 2)
    batch1 = Batch("batch1", "sku1", 20, tomorrow)
    batch2 = Batch("batch2", "sku1", 1, later)
    
    allocation = allocate(order, [batch1, batch2])
    
    assert allocation == batch1.reference
    

def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch1", "lamp", 10, eta=today)
    order = OrderLine("order1", "lamp", 11)
    
    with pytest.raises(OutOfStock, match="lamp"):
        allocate(order, [batch])
