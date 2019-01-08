(function() {

	function setup(button) {
		if (!button.dataset.origText) {
			const width = button.offsetWidth;
			button.dataset.origText = button.textContent;
			button.dataset.origClass = button.className;
			button.textContent = 'Are you sure?'
			button.className = "btn btn-warning"
			if (button.dataset.extra)
				button.className += ' ' + button.dataset.extra;
			button.style.minWidth = '' + width + 'px';
			button.dataset.timer = setTimeout(reset, 6000, button);
			return true;
		}
		return false;
	}

	function reset(button) {
		if (button.dataset.origText) {
			clearTimeout(button.dataset.timer);
			button.textContent = button.dataset.origText;
			button.className = button.dataset.origClass;
			delete button.dataset.origText;
			delete button.dataset.origClass;
			delete button.dataset.timer;
		}
	}

	function click_handler(evt) {
		if (setup(this)) {
			evt.preventDefault();
			return false;
		}
	}

	function leave_handler(evt) {
		reset(this);
	}

	window.addEventListener('load', function() {
		const elements = document.getElementsByClassName('are-you-sure');
		for (var i = 0; i < elements.length; i++) {
			const button = elements[i];
			button.addEventListener('click', click_handler);
			button.addEventListener('mouseleave', leave_handler);
		}
	});

})();
