$(document).ready(function() {
	var questionList = (("{{question_list}}").replace(/&(l|g|quo)t;/g, function(a,b){
                return {
                    l   : '<',
                    g   : '>',
                    quo : '"'
                }[b];
            }));
	var questiondata = JSON.parse(questionList);

	function updateNumbers(){
		document.getElementById("unvis").innerHTML=$(".not_visited").length-1;
		document.getElementById("locke").innerHTML=$(".locked").length-1;
		document.getElementById("unans").innerHTML=$(".unanswered").length-1;
		document.getElementById("revie").innerHTML=$(".review").length-1;
	}

	function show_hide_buttons(){
		var ques_no = parseInt(document.getElementById("questionno").innerHTML);
	}

	function load_question(next, status="unanswered", ques=false, circle=false) {
		div = document.getElementById("questionno");
		var ques_no = parseInt(div.innerHTML);

		if(ques!=false){
			ques_no = ques;
		}
		else{
		if (ques_no<parseInt("{{totalques}}") && next==1){
			ques_no++;
		}
		else{
			if (ques_no!=1 && next!=1)
				ques_no--;
		}
		}

		$("#skip").show();
		$("#previous").show();
		if(ques_no==1){
			$("#previous").hide();

		}
		console.log(ques_no);
		div.innerHTML=ques_no+"";
		statementdiv = document.getElementById("statement");
		statementdiv.innerHTML = questiondata[ques_no-1]["statement"];
		optionsdiv = document.getElementById("options");
		options = "";
		
		var ques_no_div = document.getElementById("question_pk");
		
		ques_no_div.innerHTML=questiondata[ques_no-1]["pk"];
		if(ques_no==parseInt("{{totalques}}")){
			$("#skip").hide();
		}





		
		
		for (index = 0; index < questiondata[ques_no-1]["options"].length; ++index) {
			options+="<input type='radio' name='selected_option' value='"+ questiondata[ques_no-1]["options"][index]["pk"] +"'/>";
 		   	options+="&nbsp;<b>"+"ABCDEFGHIJKLMNOPQRSTUVWXYZ"[index]+"</b>)&nbsp;"+questiondata[ques_no-1]["options"][index]["value"]+"<br/>";
		}
		optionsdiv.innerHTML=options;
		$.ajax({
                url: "/tests/status/",
                type: 'POST',
                data: {'questionpk': parseInt(ques_no_div.innerHTML), 'responsepk': parseInt("{{response.pk}}")},
                headers: { "X-CSRFToken": "{% csrf_token %}" },
                success: function(result) {
               		status = result['status']; 
               		if(status=="not_visited"){
               			status="unanswered";
               			$.ajax({
                url: "/tests/mark/",
                type: 'POST',
                data: {'status': status, 'questionpk': parseInt(ques_no_div.innerHTML), 'responsepk': parseInt("{{response.pk}}"), 'testpk': parseInt("{{test.pk}}")},
                headers: { "X-CSRFToken": "{% csrf_token %}" },
                success: function(result2) {
                	if(!circle){
                		circle=document.getElementById(""+(ques_no));
                	}
                    if(circle){
                    	$(circle).removeClass();
                    	$(circle).addClass('question');
                    	$(circle).addClass(status);
                    	$(".highlighted").removeClass('highlighted');
				       	$(circle).addClass('highlighted');
				       	updateNumbers();
                    }
                }
            });
               		}
                }
            });
		circle=document.getElementById(""+(ques_no));
		$(".highlighted").removeClass('highlighted');
       	$(circle).addClass('highlighted');
		show_hide_buttons();
		updateNumbers();
	}

	$("#skip").click(function(e) {
		load_question(1);
	});
	$("#previous").click(function(e){
		load_question(0);
	});
	$("#previous").hide();
	// $.ajax({
 //                url: "/tests/mark/",
 //                type: 'POST',
 //                data: {'status': "unanswered", 'questionpk': parseInt("{{questions.0.pk}}"), 'responsepk': parseInt("{{response.pk}}"), 'testpk': parseInt("{{test.pk}}")},
 //                headers: { "X-CSRFToken": "{% csrf_token %}" },
 //                success: function(result) {
                    
 //                }
 //            });
	$(".question").click(function(e){
		updateNumbers();
		load_question(2, "unanswered", this.id, this);
	});


	$("#1").addClass("highlighted");
	updateNumbers();
});