(function() {

	/* Iframe disabling */

	function same_origin(text) {
		const a = document.createElement('a');
		a.href = text;
		const current = window.location.protocol + '://' + window.location.host;
		const test = a.protocol + '://' + a.host;
		a.remove();
		return current == test;
	}

	function enable_iframe(form, iframe, notice) {
		if (form.target != iframe.name) {
			form.target = iframe.name;
			iframe.style.display = '';
			notice.style.display = 'none';
		}
	}

	function disable_iframe(form, iframe, notice) {
		if (form.target == iframe.name) {
			form.target = '_blank';
			iframe.style.display = 'none';
			notice.style.display = '';
		}
	}

	window.addEventListener('load', function() {
		const force = document.getElementById('disable_iframe');
		const form = document.getElementById('request-form');
		const iframe = document.getElementById('request-frame');
		const notice = document.getElementById('request-notice');
		const service_in = document.getElementById('service');

		service_in.addEventListener('change', function() {
			if (force.checked) return; // don't react with force
			if (same_origin(service_in.value)) {
				enable_iframe(form, iframe, notice);
			} else {
				disable_iframe(form, iframe, notice);
			}
		});
		force.addEventListener('change', function() {
			if (this.checked || !same_origin(service_in.value)) {
				disable_iframe(form, iframe, notice);
			} else {
				enable_iframe(form, iframe, notice);
			}
		});
		if (force.checked)
			disable_iframe(form, iframe, notice);
	});


	/* Random id generation */

	function get_random_number(min, max) {
		const range = max - min;
		return Math.floor(Math.random() * range) + min;
	}

	function get_random_string(len) {
		var text = "";
		const possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
		for (var i = 0; i < len; i++)
			text += possible.charAt(Math.floor(Math.random() * possible.length));
		return text;
	}

	function add_input_button(input, init_button) {
		if (!input) return;
		const group = document.createElement('div');
		group.setAttribute('class', 'input-group');
		input.parentNode.replaceChild(group, input);
		group.appendChild(input);
		const append = document.createElement('div');
		append.setAttribute('class', 'input-group-append');
		group.appendChild(append);
		const button = document.createElement('button');
		button.setAttribute('class', 'btn btn-outline-secondary');
		button.setAttribute('type', 'button');
		append.appendChild(button);
		init_button(button, input);
	}

	window.addEventListener('load', function() {
		add_input_button(document.getElementById('pid'), function(button, input) {
			button.classList.add('icon');
			button.classList.add('icon-dice');
			button.addEventListener('click', function() {
				input.value = get_random_string(get_random_number(4, 20));
			});
		});
		add_input_button(document.getElementById('amount'), function(button, input) {
			button.classList.add('icon');
			button.classList.add('icon-dice');
			button.addEventListener('click', function() {
				input.value = get_random_number(1, 1000);
			});
		});
	});

})();
