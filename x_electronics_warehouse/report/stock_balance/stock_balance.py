import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "X Item", "width": 200},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "X Warehouse", "width": 200},
        {"label": "Quantity", "fieldname": "quantity", "fieldtype": "Float", "width": 120},
        {"label": "Stock Value", "fieldname": "stock_value", "fieldtype": "Currency", "width": 150}
    ]
    
    data = frappe.db.sql("""
        SELECT 
            item,
            warehouse,
            SUM(quantity) as quantity
        FROM `tabX Stock Ledger Entry`
        GROUP BY item, warehouse
        HAVING quantity != 0
    """, as_dict=1)
    
    for row in data:
        row["stock_value"] = row["quantity"] * 100
    
    return columns, data
