function digits_only(input_id)
{
	let input_obj = document.getElementById(input_id);
	if (input_obj) {
		if (!/^[0-9]*$/.test(input_obj.value)) {
			let new_value = '';
			for (let i = 0; i < input_obj.value.length; i++) {
				let char = input_obj.value.charAt(i);
				if (char >= '0' && char <= '9') {
					new_value += char;
				}
			}
			input_obj.value = new_value;
		}
	}
}

function strip_zeroes(input_id, default_num=0)
{
	let input_obj = document.getElementById(input_id);
	if (input_obj) {
		if (input_obj.value === null || input_obj.value === '') {
			input_obj.value = default_num.toString();
		} else {
			input_obj.value = parseInt(input_obj.value, 10).toString();
		}
	}
}