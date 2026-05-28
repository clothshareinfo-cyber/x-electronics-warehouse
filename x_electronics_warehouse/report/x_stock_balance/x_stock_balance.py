import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"label": _("Item"), "fieldname": "item", "fieldtype": "Link", "options": "X Item", "width": 200},
        {"label": _("Warehouse"), "fieldname": "warehouse", "fieldtype": "Link", "options": "X Warehouse", "width": 200},
        {"label": _("Quantity"), "fieldname": "quantity", "fieldtype": "Float", "width": 120},
        {"label": _("Avg Rate"), "fieldname": "avg_rate", "fieldtype": "Currency", "width": 120},
        {"label": _("Stock Value"), "fieldname": "stock_value", "fieldtype": "Currency", "width": 150}
    ]
    
    data = frappe.db.sql("""
        SELECT 
            sled.item,
            sled.warehouse,
            SUM(sled.quantity) as quantity,
            AVG(CASE WHEN sled.incoming_rate > 0 THEN sled.incoming_rate ELSE NULL END) as avg_rate
        FROM `tabX Stock Ledger Entry` sled
        GROUP BY sled.item, sled.warehouse
        HAVING quantity != 0
    """, as_dict=1)
    
    for row in data:
        row["stock_value"] = (row.quantity or 0) * (row.avg_rate or 0)
    
    return columns, data
