from datetime import date, timedelta
import pytest

# from model import ...
from model import OrderLine, Batch

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def make_batch_and_line(sku, batch_qty, line_qty):
    return (Batch("batch-001", sku, batch_qty, today),
            OrderLine("order-123", sku, line_qty))


def test_allocating_to_a_batch_reduces_the_available_quantity():
    order = OrderLine("order1", "sku1", 2)
    batch = Batch("batch1", "sku1", 20)
    
    batch.allocate(order)
    
    assert batch.available_qty == 18


def test_can_allocate_if_available_greater_than_required():
    order = OrderLine("order1", "sku1", 2)
    batch = Batch("batch1", "sku1", 20)
    
    assert batch.can_allocate(order)


def test_cannot_allocate_if_available_smaller_than_required():
    order = OrderLine("order1", "sku1", 2)
    batch = Batch("batch1", "sku1", 1)
    
    assert not batch.can_allocate(order)


def test_can_allocate_if_available_equal_to_required():
    order = OrderLine("order1", "sku1", 2)
    batch = Batch("batch1", "sku1", 2)
    
    assert batch.can_allocate(order)
    
    
def test_cannot_allocalate_if_skus_dont_match():
    order = OrderLine("order1", "sku1", 2)
    batch = Batch("batch1", "sku2", 2)
    
    assert not batch.can_allocate(order)
    
    

def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("RED-LAMP", 20, 2)
   
    assert not batch.can_deallocate(unallocated_line)

    
def test_can_deallocate_allocated_lines():
    batch, line = make_batch_and_line("RED-LAMP", 20, 2)
    
    batch.allocate(line)
    batch.deallocate(line)
    
    assert batch.available_qty == 20
    
def test_allocation_is_idempotent():
    batch, line = make_batch_and_line("RED-LAMP", 20, 2)
    
    batch.allocate(line)
    batch.allocate(line)
    
    assert batch.available_qty == 18
    
    
def test_batch_identified_by_reference():
    batch1 = Batch("batch1", "sku2", 20, tomorrow)
    batch2 = Batch("batch1", "sku1", 1, later)
    
    assert batch1 == batch2
    