"use strict";

let Email = {
	is_valid_address: function(email)
	{
		if (email == '') {
			return true;
		}
		
		if (email.indexOf('@') < 0) {
			return false;
		}
		let address = {
			local: '',
			domain: ''
		};
		// First, split into local and domain parts
		let is_domain = false;
		for (let i = email.length - 1; i >= 0; i--) {
			if (!is_domain) {
				if (email.charAt(i) == '@') {
					is_domain = true;
				} else {
					address.domain = email.charAt(i) + address.domain;
				}
			} else {
				address.local = email.charAt(i) + address.local;
			}
		}
		
		return (this._is_valid_local(address.local) && this._is_valid_domain(address.domain));
	},
	
	_is_valid_local: function(local)
	{
		if (local.length == 0 || local.length > 64) {
			return false;
		}
		
		if (!/^[\x20-\x7E]*$/.test(local)) {
			return false;
		}
		
		if (local.charAt(0) == '"' && local.charAt(local.length - 1) == '"' && local.length > 1) {
			// For quoted local parts, more characters are allowed
			let quoted = local.substr(1, local.length - 2).split('\\\\').join('');
			if (quoted == '') {
				return true;
			}
			if (quoted.charAt(quoted.length - 1) == '\\') {
				return false;
			}
			
			let backslash = false;
			for (let i = 0; i < quoted.length; i++) {
				if (backslash) {
					backslash = false;
				} else {
					if (quoted.charAt(i) == '\\') {
						backslash = true;
					} else if (quoted.charAt(i) == '"') {
						return false;
					}
				}
			}
			
		} else {
			if (local.charAt(0) == '.' || local.charAt(local.length - 1) == '.') {
				return false;
			}
			
			let last_dot = false;
			for (let i = 0; i < local.length; i++) {
				let c = local.charAt(i);
				if (c == ' ' || c == '"' || c == '(' || c == ')' || c == ',' || c == ':' || c == ';' || c == '<' || c == '>' || c == '@' || c == '[' || c == '\\' || c == ']') {
					return false;
				}
				if (last_dot) {
					if (c == '.') {
						return false;
					} else {
						last_dot = false;
					}
				}
				if (!last_dot && c == '.') {
					last_dot = true;
				}
			}
		}
		
		return true;
	},
	
	_is_valid_domain: function(domain)
	{
		if (domain.length == 0 || domain.length > 255) {
			return false;
		}
		
		if (!/^[\x20-\x7E]*$/.test(domain)) {
			return false;
		}
		
		if (domain.startsWith('[') && domain.endsWith(']')) {
			let ip = domain.substr(1, domain.length - 2);
			if (ip.toLowerCase().startsWith('ipv6:')) {
				return this._is_valid_ipv6(ip.substr(5));
			} else {
				return this._is_valid_ipv4(ip);
			}
		} else {
			let subdomains = domain.split('.');
			for (let i = 0; i < subdomains.length; i++) {
				if (subdomains[i] == '') {
					return false;
				} else {
					for (let j = 0; j < subdomains[i].length; j++) {
						let c = subdomains[i].charAt(j);
						if (c == '-' && (j == 0 || j == subdomains[i].length - 1)) {
							return false;
						} else if (c != '-' && !(c >= '0' && c <= '9') && !(c >= 'a' && c <= 'z') && !(c >= 'A' && c <= 'Z')) {
							return false;
						}
					}
				}
			}
		}
		
		return true;
	},
	
	_is_valid_ipv4: function(ip)
	{
		let nums = ip.split('.');
		if (nums.length != 4) {
			return false;
		}
		for (let i = 0; i < nums.length; i++) {
			let num = nums[i];
			if (num == '' || num.length > 3) {
				return false;
			}
			if (!/^[0-9]*$/.test(num)) {
				return false;
			}
			let val = parseInt(num);
			if (val < 0 || val > 255) {
				return false;
			}
		}
		
		return true;
	},
	
	_is_valid_ipv6: function(ip)
	{
        let hexs = ip.split(':');
		if (hexs.length == 0 || hexs.length > 8) {
			return false;
		}
		if (ip.indexOf(':::') >= 0) {
			return false;
		}
		if (hexs.length < 8 && ip.indexOf('::') < 0) {
			return false;
		}
		
		let occurrences = (ip.match(/::/g) || []).length;
		if (occurrences > 1) {
			return false;
		}
		
		for (let i = 0; i < hexs.length; i++) {
			let hex = hexs[i];
			if (hex.length > 4) {
				return false;
			}
			if (!/^[0-9a-fA-F]*$/.test(hex)) {
				return false;
			}
		}
		
		return true;
	}
};