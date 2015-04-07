//references to the timers updating the GUI.
var updateTimer;
var delayTimer;

var GUI = {

	InitLayoutSetUp : function(){

		$(".btnChangeCollection").hide();
		$(".imageCollection").hide();
		$(".imageCollection").eq(0).show();
		$(".tagLabel").eq(0).css("color", "black");

		$(".btnChangeCollection").mouseleave(function(){

			$(this).css("background-color", "#lightgray");
		});

		$("#preview").hover(
			function(){
				$(".btnChangeCollection").fadeIn("fast");
			},
			function(){
				$(".btnChangeCollection").fadeOut("fast");
			});
	},

	SetInitListeners : function(){

		$(".btnChangeCollection").click(function(){

			var boolMoveLeft = (this.id == "btnLeft");

			clearInterval(updateTimer);
			clearTimeout(delayTimer);
			GUI.Update(boolMoveLeft, 5);
			delayTimer = setTimeout(function(){
				updateTimer = window.setInterval(GUI.Update, 3000, false, 600);
			}, 4000);
		});	

		$(".smallImage").click(function(){

			var state = $("#state").attr("content");			
			var picParams = { id : $(this).attr("id"), tagName : $(this).parent().attr("id") };
			var tagParams = { tagName : $(this).parent().attr("id") }

			$(".message").text("Laddar");
			$(".loading").css("opacity", "1");

			$(".largeImage").remove();
			$(".imageWithTag").remove();
			Request.Get(state + "Tag", tagParams, GUI.DisplayTaggedImages);
			Request.Get(state + "Image", picParams, GUI.DisplayLargeImage);
		});

		$("#updateContainer").click(function(){
			$("#rotateParagraph").addClass("spin");
		});
	},

	DisplayLargeImage : function(imageJson){

		if($("#largeImageContainer").width() > 1000){
			$("#largeImageContainer").animate({
				width  : "52%" 
			}, 500);
		}

		var image = document.createElement("img");
		var prefix = ($("#state").attr("content") == "local")? "/static/" : "";
		image.setAttribute("src", prefix + imageJson.bigURL);
		image.setAttribute("class", "largeImage");

		$("#largeImageContainer").animate({

				height : 60 + parseInt(imageJson.bigHeight)
			}, 500);


		$("#largeImageContainer>#displayer").fadeOut("fast", function(){
			$(".largeImage").remove();
			$("#largeImageContainer>#displayer").append(image);
			var title =  "\"" + imageJson.title +"\"" ;
			var user = imageJson.user;
			$("#picInfo").text(title + " av " + user);
			$(".largeImage").css("margin-left", -(imageJson.bigWidth/2))
			$(this).fadeIn("fast");

		});
		$("#largeImageContainer>.userInfo").css("display", "none");

	},

	DisplayTaggedImages : function(tag){

		$("#imagesWithTagContainer>#container").fadeOut(5, function(){

			$(".imageWithTag").remove();
			var prefix = ($("#state").attr("content") == "local")? "/static/" : "";

			for (var i = 0; i< tag.images.length; i++) {
				var image = document.createElement("img");
				image.setAttribute("src", prefix + tag.images[i].url);
				image.setAttribute("class", "imageWithTag");
				image.setAttribute("id", tag.images[i].id);
				$("#imagesWithTagContainer>#container").append(image);
			}

			var odd = (tag.images.length % 3 == 0)? 0 : 1;
			var nrOfRows = Math.round(tag.images.length/3) + odd; 
			$("#imagesWithTagContainer").animate({
				"height" : 160 * nrOfRows + 100
				}, 500);

			$(this).delay(500).fadeIn("slow");
			$(".imageWithTag").click(function(){
				$(".largeImage").remove();
				Request.Get($("#state").attr("content") + "Image", 
							{ id : $(this).attr("id"), tagName : tag.tagName }, 
							GUI.DisplayLargeImage);
			});
		});

		$("#imagesWithTagLabel").text("Bilder taggade med \"" + tag.tagName + "\"");


	},
	
	CalculateNextIndex : function(boolMoveLeft){

		var currentIndex = $(".imageCollection").index($(".imageCollection:visible"));
		var nextIndex;

		if(boolMoveLeft){

			nextIndex =  currentIndex > 0 ? currentIndex-1 : $(".imageCollection").size()-1;
						
		}else{

			nextIndex =  currentIndex < $(".imageCollection").size()-1 ? currentIndex+1 : 0;
		}

		return nextIndex;
	},

	Update : function(boolMoveLeft, speed){

		var currentIndex = $(".imageCollection").index($(".imageCollection:visible"));
		var nextIndex = GUI.CalculateNextIndex(boolMoveLeft);

		GUI.ChangeVisibleImageCollection(currentIndex, nextIndex, speed);
		GUI.ChangeActiveTagName(currentIndex, nextIndex);

	},

	ChangeVisibleImageCollection : function(currentIndex, nextIndex, speed){

		$(".imageCollection").eq(currentIndex).fadeOut(speed);
		$(".imageCollection").eq(nextIndex).fadeIn(speed);
		
	},

	ChangeActiveTagName : function(currentIndex, nextIndex){

		$(".tagLabel").eq(currentIndex).css("color", "lightgray");
		$(".tagLabel").eq(nextIndex).css("color", "black");

	}
};

var Request = {

	Get : function(url, data, callback){

		$.get(url, data, function(data,status){

					console.log(data);
					json = jQuery.parseJSON(data);	
					callback(json);
		});
	}
} 

$(document).ready(function(){

	GUI.InitLayoutSetUp();
	GUI.SetInitListeners();

	updateTimer = window.setInterval(GUI.Update, 3000, false, 600);

	$(window).unload(function(){
		
	});
	
});


