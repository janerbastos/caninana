$('#form_modal_ajax').on('show.bs.modal', function(event) {
	var button = $(event.relatedTarget);

	var content_type = button.data('content_type');
	var url = button.data('url');
	var _action = button.data('action');
	var object = button.data('object');

	var modal = $(this);
	var form = modal.find('form');
	var action = form.attr('action');

	if (!action.endsWith('/')) {
		action += '/';
	}

	if (object) {
        _request_get = '?' + _action + '=' + content_type + '&object=' + object;
    }
    else{
        _request_get = '?' + _action + '=' + content_type;
    }

    form.attr('action', url + _request_get);
	if (_action=='@@removeObject') {
        data = {
            '@@removeObject': content_type,
            '@@object': object,
        }
    }else{
	    data = {
            '@@createObject': content_type,
            '@@object': object,
        }
    }
    ajax_form_request(url, data, modal);
});


function ajax_form_request(url, data, modal) {
    $.ajax({
        url: url,
        data: data,
        dataType: 'json',
        success: function (data) {
            modal.find('.modal-body p').html(data.result);
            modal.find('.modal-title').html(data.sessao);
        }
    });
}
