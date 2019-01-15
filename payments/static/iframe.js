(function() {
	function current_script() {
		if (document.currentScript) {
			return document.currentScript;
		} else {
			const scripts = document.getElementsByTagName('script');
			return scripts[scripts.length-1];
		}
	}

	function empty(elem) {
		while (elem.firstChild) {
			elem.removeChild(elem.firstChild);
		}
	}

	function add_url_input_to(nav) {
		const elem = document.createElement("input");
		elem.setAttribute('class', 'form-control mr-sm-2');
		elem.setAttribute('type', 'url');
		elem.setAttribute('aria-label', 'url');
		elem.setAttribute('value', window.location.href);
		elem.setAttribute('readonly', 'readonly');
		nav.appendChild(elem);
	}

	window.addEventListener('load', function() {
		if (window.location !== window.parent.location) {
			const nav = document.getElementById('page-nav');
			if (nav) {
				empty(nav);
				add_url_input_to(nav);
			}
			const footer = document.getElementById('page-footer');
			if (footer) empty(footer);
		}
	});
})();
