/**
 * 
Jqeury validator
$(document).ready(function(){
	$('#write_form').validate({
		rules:{
			title: { required: true },
			tags: { required: true },
			content: { required: true},
		},
		messages:{
			title:{
				required: "제목을 입력하시오."
			},
			tags:{
				required: "카테고리를 입력하시오"
			},					
			content:{
				required: "내용을 입력하시오"
			}
		}
			
	})

})
 */

$(document).ready(function() {
    $('#write_form').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
        	title: {
                message: 'The title is not valid',
                validators: {
                    notEmpty: {
                        message: 'The title is required and cannot be empty'
                    }
                }
            },
            tags: {
                validators: {
                    notEmpty: {
                        message: 'The tags is required and cannot be empty'
                    }
                }
            },
            content: {
                validators: {
                    notEmpty: {
                        message: 'The contents is required and cannot be empty'
                    }
                }
            }
            
        }
    });
    
    $('#loginform').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
		    name: {
		        validators: {
                    notEmpty: {
                        message: 'The username is required and cannot be empty'
                    },
                    different: {
                        field: 'password',
                        message: 'The username and password cannot be the same as each other'
                    }
		        }
		    },
		    password: {
		        validators: {
		            notEmpty: {
		                message: 'The password is required and cannot be empty'
		            }
			    }
	        }
        }
    });
    

    $('#joinform').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            name: {
                message: 'The username is not valid',
                validators: {
                    notEmpty: {
                        message: 'The username is required and cannot be empty'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'The username must be more than 6 and less than 30 characters long'
                    },
                    different: {
                        field: 'password',
                        message: 'The username and password cannot be the same as each other'
                    }
                }
            },
		    email: {
		        validators: {
		            notEmpty: {
		                message: 'The email address is required and cannot be empty'
		            },
		            emailAddress: {
		                message: 'The email address is not a valid'
		            }
		        }
		    },
            password: {
                validators: {
                    notEmpty: {
                        message: 'The password is required and cannot be empty'
                    },
                    different: {
                        field: 'username',
                        message: 'The password cannot be the same as username'
                    },
                    stringLength: {
                        min: 8,
                        message: 'The password must have at least 8 characters'
                    },
                    identical: {
                                field: 'password',
                                message: 'The password and its confirm are not the same'
                    }                   
                }
            },
            password2: {
                validators: {
                    notEmpty: {
                        message: 'The password is required and cannot be empty'
                    },
                    stringLength: {
                        min: 8,
                        message: 'The password must have at least 8 characters'
                    },
                    identical: {
                                field: 'password',
                                message: 'The password and its confirm are not the same'
                    }                   
                }
            },
        }
    });

});



var checkJoinName = function(A){	
	var name = $(A).val();

    $.ajax({
    	url : '/join',
    	type : 'POST',
    	data : {"name" : name
    	},    	    	
    	success : function(data1){
    		console.log(data1);
    		var _result = data1;

            if(_result == 'False'){
                    $('#duplicatedname2').css('display','none');
                    $('#duplicatedname1').css('display','');
                }else{
                    $('#duplicatedname1').css('display','none');
                    $('#duplicatedname2').css('display','');
            }
    	} 
    })
}

var checkJoinEmail = function(A){	
	var email = $(A).val();
	console.log(email);
	// email check
    $.ajax({
    	url : '/join',
    	type : 'POST',
    	data : {"email" : email    			
    	},    	    	
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
