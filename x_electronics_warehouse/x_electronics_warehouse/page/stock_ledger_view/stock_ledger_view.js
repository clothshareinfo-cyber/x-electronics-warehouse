frappe.pages['stock-ledger-view'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Stock Ledger Report',
		single_column: true
	});
}