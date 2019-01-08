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
		const t = document.createTextNode(format(data.text, expires));
		data.textbox.appendChild(t);
		if (expires > 0) {
			setTimeout(update_timed_press, 1000, data, expires-1);
		} else {
			data.button.click();
		}
	}

	function add_timed_press(button, expires) {
		const badge = document.createElement('span');
		badge.setAttribute('class', 'badge badge-dark');
		button.appendChild(document.createTextNode(' '));
		button.appendChild(badge);
		const i = document.createElement('i');
		i.setAttribute('class', 'fas fa-stopwatch');
		badge.appendChild(i);
		const text = document.createElement('span');
		badge.appendChild(text);
		const data = {
			button: button,
			badge: badge,
			textbox: text,
			text: " {0}s",
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
