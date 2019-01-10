(function() {

	function format() {
		var formatted = arguments[0];
		for (var i = 0; i < arguments.length-1; i++) {
			const regexp = new RegExp('\\{'+i+'\\}', 'g');
			formatted = formatted.replace(regexp, arguments[i+1]);
		}
		return formatted;
	}

	function empty(elem) {
		while (elem.firstChild) {
			elem.removeChild(elem.firstChild);
		}
	}


	/* Automatic forward to not let jwt token expire */

	function for_submits(elem, action) {
		const buttons = elem.getElementsByTagName('button');
		for (var i = 0; i < buttons.length; i++) {
			const button = buttons[i];
			if (button.type.toLowerCase() == 'submit') {
				action(button);
			}
		}

	}

	function update_timed_press(data, expires) {
		empty(data.textbox);
		data.textbox.appendChild(document.createTextNode(expires));
		if (expires > 0) {
			setTimeout(update_timed_press, 1000, data, expires-1);
		} else {
			data.button.click();
		}
	}

	function add_timed_press(button, expires) {
		const badge = document.createElement('span');
		badge.setAttribute('class', 'badge badge-dark  icon icon-stopwatch');
		button.appendChild(document.createTextNode(' '));
		button.appendChild(badge);
		const text = document.createElement('span');
		badge.appendChild(document.createTextNode(' '));
		badge.appendChild(text);
		badge.appendChild(document.createTextNode('s'));
		const data = {
			button: button,
			badge: badge,
			textbox: text,
		};
		update_timed_press(data, expires)
	}

	window.addEventListener('load', function() {
		const elements = document.getElementsByClassName("press-automatically");
		for (var i = 0; i < elements.length; i++) {
			const element = elements[i];
			const expires = element.dataset.expireIn;
			if (expires) {
				for_submits(element, function(button) {
					add_timed_press(button, expires);
				});
			}
		}
	});


	/* Cookie policy */

	window.addEventListener('load', function() {
		const checkbox = document.getElementById("use-cookies");
		if (checkbox) {
			checkbox.addEventListener('change', function() {
				const val = checkbox.checked ? 'yes' : 'no';
				const inputs = document.getElementsByName('cookies_ok');
				for (var i = 0; i < inputs.length; i++) {
					inputs[i].value = val;
				}
			});
		}
	});

})();
