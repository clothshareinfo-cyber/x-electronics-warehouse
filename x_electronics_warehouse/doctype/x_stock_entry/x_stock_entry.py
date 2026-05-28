import frappe
from frappe.model.document import Document

class XStockEntry(Document):
    pass

@frappe.whitelist()
def on_submit(doc, method):
    """Create ledger entries when stock entry is submitted"""
    print("on_submit triggered for:", doc.name)
    
    for item in doc.items:
        if doc.purpose == "Receipt":
            create_ledger_entry(doc, item.item, item.target_warehouse, "Receipt", item.quantity, item.rate)
        elif doc.purpose == "Consume":
            create_ledger_entry(doc, item.item, item.source_warehouse, "Consume", -item.quantity, 0)
        elif doc.purpose == "Transfer":
            create_ledger_entry(doc, item.item, item.source_warehouse, "Transfer", -item.quantity, 0)
            create_ledger_entry(doc, item.item, item.target_warehouse, "Transfer", item.quantity, 0)
    
    frappe.db.set_value("X Stock Entry", doc.name, "status", "Submitted")
    frappe.db.commit()

def create_ledger_entry(doc, item, warehouse, trans_type, qty, rate):
    """Create a single ledger entry"""
    ledger = frappe.get_doc({
        "doctype": "X Stock Ledger Entry",
        "item": item,
        "warehouse": warehouse,
        "posting_date": doc.posting_date,
        "posting_time": doc.posting_time,
        "transaction_type": trans_type,
        "quantity": qty,
        "incoming_rate": rate,
        "voucher_type": "X Stock Entry",
        "voucher_no": doc.name
    })
    ledger.insert()
    ledger.db_set("docstatus", 1)
    print(f"  Ledger created: {trans_type} {qty}")
