$(document).ready(function () {
    $('.nav a').each(function() {
        var location  = window.location.protocol + '//' + window.location.host + window.location.pathname;
        var link = this.href;
        if (location == link) {
        	$(this).parent().addClass('active');
        }
    });
});