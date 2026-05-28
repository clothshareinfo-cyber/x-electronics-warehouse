# Warehouse Management System for X Electronics

Frappe App to manage inventory, track stock movements, and generate stock reports with moving average valuation

## Introduction
This app includes functionalities to manage warehouse operations, track stock movements across multiple locations, and generate real-time stock reports. The system uses a **stateless stock ledger** that calculates balances on-demand, avoiding the performance bottlenecks of traditional inventory systems.

## Key Features

### DocTypes
- **X Item**
- **X Warehouse**
- **X Stock Entry**
- **X Stock Entry Detail**
- **X Stock Ledger Entry**

### Reports
- **Stock Balance Report**
- **Stock Ledger Report**

### Technical Highlights
- Stateless Stock Ledger (no balance stored)
- Moving Average Valuation (single SQL query)
- Tree Warehouse Structure (parent-child hierarchy)
- Real-time stock calculations

---

## DocTypes

### X Item
Each product in the system should have an X Item record. This stores:
- Product code and name
- Description
- Unit of measure (Nos, Kg, Meter, etc.)
- Valuation rate (current cost)
<img width="1913" height="995" alt="Screenshot 2026-05-28 124508" src="https://github.com/user-attachments/assets/9242a13e-85f4-407f-8e31-f4c10e4f9a34" />

### X Warehouse
Tracks warehouse locations with parent-child hierarchy. Examples:
- Main Distribution Center (parent)
  - North Zone Warehouse (child)
  - South Zone Warehouse (child)
  - East Zone Warehouse (child)

Warehouses can be organized in a tree structure for multi-location inventory management.
<img width="942" height="419" alt="Screenshot 2026-05-28 145732" src="https://github.com/user-attachments/assets/50fa74d9-bf86-482c-8369-b9d9a7d4691e" />


### X Stock Entry
Records all stock movements with three purposes:

**Receipt:** Adding stock to a warehouse
- Select item, quantity, rate, and target warehouse
<img width="955" height="662" alt="Screenshot 2026-05-28 150010" src="https://github.com/user-attachments/assets/61c854ff-1aac-49fd-9d3f-c6502935b504" />

**Transfer:** Moving stock between warehouses
- Select item, quantity, source warehouse, and target warehouse
<img width="957" height="649" alt="Screenshot 2026-05-28 150158" src="https://github.com/user-attachments/assets/9ec8bf15-4a77-4483-82e4-8df84fde1ec6" />

**Consume:** Removing stock from a warehouse
- Select item, quantity, and source warehouse
<img width="946" height="652" alt="Screenshot 2026-05-28 150304" src="https://github.com/user-attachments/assets/a49efe2a-0cf8-4378-af26-3db05ead9d16" />

### X Stock Entry Detail
Child table that holds line items for each stock entry. Includes:
- Item (link to X Item)
- Quantity
- Rate (for receipts)
- Source warehouse (for transfers/consumption)
- Target warehouse (for receipts/transfers)
<img width="1658" height="924" alt="Screenshot 2026-05-28 133729" src="https://github.com/user-attachments/assets/fe82b430-d386-43aa-b04c-07d53489beb9" />

### X Stock Ledger Entry
**Stateless version** - unlike traditional ERPNext which stores actual_qty, this only records transactions:

- Item (link to X Item)
- Warehouse (link to X Warehouse)
- Posting date and time
- Transaction type (Receipt, Consume, Transfer)
- Quantity (positive for incoming, negative for outgoing)
- Incoming rate (for receipts)

No actual_qty field is stored. Balance is calculated on-demand.

<img width="941" height="554" alt="Screenshot 2026-05-28 135959" src="https://github.com/user-attachments/assets/6b167527-13cd-4c80-8333-fbc9ef05885d" />



## Reports

### Stock Balance Report
Shows current stock levels with moving average valuation.

**Features:**
- Grouped by item and warehouse
- Calculates moving average rate
- Shows total stock value
- Real-time calculation
  <img width="824" height="322" alt="Screenshot 2026-05-28 150638" src="https://github.com/user-attachments/assets/dd8c9690-357f-4234-a9c8-dcb1c8047c2e" />


### Stock Ledger Report
Shows all stock movements with running balance.

**Features:**
- Complete transaction history
- Running balance per item/warehouse
- Sortable by date
- Filterable by item and warehouse
  <img width="838" height="259" alt="Screenshot 2026-05-28 150657" src="https://github.com/user-attachments/assets/beaef42d-6c8a-4da9-b53d-1c83d60f429f" />




## Moving Average Valuation
<img width="729" height="481" alt="Screenshot 2026-05-28 150720" src="https://github.com/user-attachments/assets/79abe5e1-84c7-4c9d-b989-c444dbe68ae0" />


Moving average is calculated using a **single SQL query**:

```sql
SELECT 
    item,
    AVG(CASE WHEN incoming_rate > 0 
             THEN incoming_rate 
             ELSE NULL END) as moving_average_rate
FROM `tabX Stock Ledger Entry`
GROUP BY item
This ensures:

Only receipts affect the moving average

Zero or null rates are ignored

Weighted average is calculated automatically

Stateless Design
Traditional systems store running balances:

text
Transaction: +100 → Balance = 100 (stored)
Transaction: +50  → Balance = 150 (stored)
Transaction: -30  → Balance = 120 (stored)
This system (Stateless):

text
Only store transactions: +100, +50, -30
Calculate balance on-demand: SUM(100 + 50 - 30) = 120
Benefits:

No data duplication

Always accurate

Faster for large datasets

Easier to debug

Installation
Manual Installation
Install bench

Install ERPNext

Add the app to your bench:

bash
bench get-app https://github.com/clothshareinfo-cyber/x-electronics-warehouse.git
Install the app on your site:

bash
bench --site {sitename} install-app x_electronics_warehouse
Replace {sitename} with the name of your site

Migrate and restart:

bash
bench migrate
bench restart
Frappe Cloud Installation
Adding the App to Your Bench:

Log Into Frappe Cloud Dashboard - Access your account on Frappe Cloud

Navigate to your Bench Apps Section - Click on the Apps tab

Add New App - Click Add App button

Enter App URL: https://github.com/clothshareinfo-cyber/x-electronics-warehouse.git

Complete the Addition - Follow any additional prompts

Installing the App on a Specific Site:

Access Your Sites - Navigate to the Sites section

Select Your Site - Click on the site you want to install on

Install the App - Go to Apps tab → Click Install App

Find X Electronics Warehouse in the list and proceed with installation

Verification and Use:

Verify Installation - Check installed apps list on your ERPNext site

Use the App - Search for "X Item", "X Warehouse", or "Stock Balance" in the awesome bar

Steps for Using the System
1. Create Products (X Item)
Go to X Item → Add New

Enter item code, name, and valuation rate

Save

2. Create Warehouses (X Warehouse)
Go to X Warehouse → Add New

Create parent warehouse (leave parent blank)

Create child warehouses (select parent)

Save each warehouse

3. Add Stock (Receipt)
Go to X Stock Entry → New

Select Purpose: Receipt

Add items: select product, quantity, rate

Select target warehouse

Save → Submit

4. Move Stock (Transfer)
Go to X Stock Entry → New

Select Purpose: Transfer

Add items: select product, quantity

Select source and target warehouses

Save → Submit

5. Remove Stock (Consume)
Go to X Stock Entry → New

Select Purpose: Consume

Add items: select product, quantity

Select source warehouse

Save → Submit

6. View Reports
Stock Balance Report - See current stock levels

Stock Ledger Report - See all transactions

Testing
Run Automated Tests
bash
bench --site {sitename} run-tests --app x_electronics_warehouse
Manual Test in Console
bash
bench --site {sitename} console
python
from frappe.utils import today, nowtime

# Create a test receipt
receipt = frappe.get_doc({
    "doctype": "X Stock Entry",
    "purpose": "Receipt",
    "posting_date": today(),
    "posting_time": nowtime(),
    "items": [{
        "item": frappe.get_all("X Item")[0].name,
        "quantity": 100,
        "rate": 100,
        "target_warehouse": frappe.get_all("X Warehouse")[0].name
    }]
})
receipt.insert()
receipt.submit()
print("✓ Test successful!")
Verify Stateless Design
python
# Check that actual_qty field does NOT exist
has_actual_qty = frappe.db.exists("DocField", {
    "parent": "X Stock Ledger Entry",
    "fieldname": "actual_qty"
})
print(f"Stateless: {'✓ PASSED' if not has_actual_qty else '✗ FAILED'}")
Sample Data
When installed, you get sample data:

Products
Product	Quantity	Rate	Total Value
Gaming Laptop Pro	50	$1,500	$75,000
Wireless Mouse	50	$75	$3,750
Mechanical Keyboard	50	$120	$6,000
27 Inch Monitor	250	$1,150	$287,500
Total Inventory Value: $372,250

Warehouse Structure
text
Main Distribution Center (Parent)
├── North Zone Warehouse
├── South Zone Warehouse
└── East Zone Warehouse
Requirements Checklist
Item/Product DocType

Warehouse (Tree) DocType

Stateless Stock Ledger Entry (no actual_qty field)

Moving Average Valuation (Single SQL Query)

Stock Entry - Receipt operation

Stock Entry - Consume operation

Stock Entry - Transfer operation

Stock Ledger Report (movement on each line)

Stock Balance Report (consolidated with moving average)

Unit Tests covering all functionality

Author
John Kariuki

GitHub: @clothshareinfo-cyber

License
MIT

Built for X Electronics | Complete Warehouse Management Solution
