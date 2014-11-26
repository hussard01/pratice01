var toggle_comment_box = function(url, entry_id){
	
	var el = $('#comment_box_'+entry_id);
	
	if(el.is(":visible")){
		el.hide();
	}else{		
		$.ajax({
			url : url,
			success : function(data){
				el.append(data);
			}		
		});
		el.show();
	}
}

var add_comment = function(form_el){
	
	var form_el = $(form_el);
	
    $.ajax({
    	url : '/blog/add/comment',
    	type : 'POST',
    	data : form_el.serialize(),
    	dataType: 'json',
    	success : function(data){
    		var _result = data;
    		$('#comment_box_'+_result['entry_id']).empty();
    		$('#comment_box_'+_result['entry_id']).prepend(_result['msg']);
    		/*
    		if (req.responseText.isJSON() == true ) {
                var _result = req.responseText.evalJSON(true);
                $('#comment_box_'+_result['entry_id']).append(_result['msg']);
            }
            else {
                alert(req.responseText);
            } 
            */   		
    	} 
    })     
}

var del_comment = function(button){	
	$(button).closest('#del_comment').find('#password_form').slideDown('slow', function(){	
		$(this).css('display', '');
	});
	$(button).remove();
}