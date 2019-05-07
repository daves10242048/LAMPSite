//// use "input_format.js"

function set_filter_button(filter_button_id, input_id, set_error=false)
{
	let filter_button_obj = document.getElementById(filter_button_id);
	let input_obj = document.getElementById(input_id);
	if (filter_button_obj && input_obj) {
		if (!/^[0-9]+$/.test(input_obj.value)) {
			filter_button_obj.disabled = true;
			if (set_error) {
				input_obj.classList.add('ierror');
			}
		} else if (parseInt(input_obj.value) < 1 || parseInt(input_obj.value) > 100) {
			filter_button_obj.disabled = true;
			if (set_error) {
				input_obj.classList.add('ierror');
			}
		} else {
			filter_button_obj.disabled = false;
			input_obj.classList.remove('ierror');
		}
	}
}

function apply_filter(input_id, sort_id, order_id, button_id)
{
	let input_obj = document.getElementById(input_id);
	let sort_obj = document.getElementById(sort_id);
	let order_obj = document.getElementById(order_id);
	let button_obj = document.getElementById(button_id);

	if (input_obj && sort_obj && order_obj && button_obj) {
		let count = input_obj.value;
		let sort = sort_obj.options[sort_obj.selectedIndex].value;
		let order = order_obj.options[order_obj.selectedIndex].value;

		button_obj.disabled = true;
		input_obj.readOnly = true;
		sort_obj.readOnly = true;
		order_obj.readOnly = true;
		window.location.href = window.location.pathname + '?count=' + count + '&sort=' + sort + '&order=' + order;
	}
}