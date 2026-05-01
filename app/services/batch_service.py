# app/services/batch_service.py

class BatchProcessor:
    def __init__(self):
        self.pending_orders = []

    def add_order(self, order):
        self.pending_orders.append(order)

    def get_batch(self):
        return self.pending_orders

    def clear(self):
        self.pending_orders = []

batch_processor = BatchProcessor()