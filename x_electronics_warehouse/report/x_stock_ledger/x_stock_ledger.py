import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": _("Time"), "fieldname": "posting_time", "fieldtype": "Time", "width": 100},
        {"label": _("Item"), "fieldname": "item", "fieldtype": "Link", "options": "X Item", "width": 150},
        {"label": _("Warehouse"), "fieldname": "warehouse", "fieldtype": "Link", "options": "X Warehouse", "width": 150},
        {"label": _("Type"), "fieldname": "transaction_type", "fieldtype": "Data", "width": 100},
        {"label": _("Qty"), "fieldname": "quantity", "fieldtype": "Float", "width": 80},
        {"label": _("Balance"), "fieldname": "balance_qty", "fieldtype": "Float", "width": 100}
    ]
    
    entries = frappe.db.get_all("X Stock Ledger Entry", 
        fields=["posting_date", "posting_time", "item", "warehouse", "transaction_type", "quantity"],
        order_by="posting_date ASC, posting_time ASC")
    
    balance = {}
    data = []
    for e in entries:
        key = f"{e.item}_{e.warehouse}"
        balance[key] = balance.get(key, 0) + e.quantity
        data.append({
            "posting_date": e.posting_date,
            "posting_time": e.posting_time,
            "item": e.item,
            "warehouse": e.warehouse,
            "transaction_type": e.transaction_type,
            "quantity": e.quantity,
            "balance_qty": balance[key]
        })
    
    return columns, data
