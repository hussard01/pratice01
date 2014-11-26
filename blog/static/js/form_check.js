/**
 * 
 */

var checkJoinForm = function(A){	
	var email = $(A).val();
	console.log(email);
	// email check
    $.ajax({
    	url : '/join',
    	type : 'POST',
    	data : {"email" : email},    	
    	success : function(data1){
    		console.log(data1);
    		var _result = data1;
    		if(_result == 'False'){  		    		
    			$('#duplicatedemail2').css('display','none');
    			$('#duplicatedemail1').css('display','');
    		}else{    			
    			$('#duplicatedemail1').css('display','none');
    			$('#duplicatedemail2').css('display','');    			
    		}
    	} 
    })   
	
	
}