var toggle_comment_box = function(url, entry_id){
	var el = $('comment_box_'+entry_id);
	
	if(el.visible() == true){
		el.hide();
	}else{
		var ajax = new Ajax.Updater(el, url);
		el.show();
	}
}

var add_comment = function(form_el){
	var form_el = $(form_el);
	 
	    var ajax = new Ajax.Request(form_el.action, {
	                method: form_el.method,
	                parameters: form_el.serialize(),
	                onSuccess: function(req) {
	                    if ( req.responseText.isJSON() == true ) {
	                        var _result = req.responseText.evalJSON(true);
	                        $('comment_box_'+_result['entry_id']).update(_result['msg']);
	                    }
	                    else {
	                        alert(req.responseText);
	                    }
	                },
	                onFailure: function(req) {
	                }
	  });
}
