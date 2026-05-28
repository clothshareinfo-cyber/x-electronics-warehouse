frappe.pages['stock-balance-view'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Stock Balance Report',
		single_column: true
	});
}