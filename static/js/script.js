function fetchdata(){
    text = $("#text_editor").val();
    console.log(text);
    $.ajax({
	type : 'POST',
	url : "/post",//"{{url_for('post')}}",
	contentType: 'application/json;charset=UTF-8',
	dataType: "json",
	data : JSON.stringify({"data":text}),
	success: function(response){
	    // Perform operation on the return value
	    checks = document.getElementById("checks");
	    checks.innerHTML = response['text']
	    console.log(response);
	}
 });
}

$(document).ready(function(){
 setInterval(fetchdata,1000);
});
