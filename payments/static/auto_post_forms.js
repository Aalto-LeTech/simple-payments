(function() {
	window.addEventListener('load', function() {
		const forms = document.getElementsByTagName('form');
		for (var i = 0; i < forms.length; i++) {
			forms[i].submit();
		}
	});
})();
