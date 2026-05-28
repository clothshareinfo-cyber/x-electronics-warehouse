import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"label": "Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "X Item", "width": 150},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "X Warehouse", "width": 150},
        {"label": "Type", "fieldname": "transaction_type", "fieldtype": "Data", "width": 100},
        {"label": "Quantity", "fieldname": "quantity", "fieldtype": "Float", "width": 100}
    ]
    
    data = frappe.db.get_all("X Stock Ledger Entry",
        fields=["posting_date", "item", "warehouse", "transaction_type", "quantity"],
        order_by="posting_date asc")
    
    return columns, data
