frappe.pages['warehouse-list'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Warehouse List',
		single_column: true
	});
}