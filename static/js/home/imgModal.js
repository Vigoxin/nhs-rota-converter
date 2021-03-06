if ($('#myModal').length) {
	function changeImage() {
		$('.rota-screenshot').css("display", "none");
		hospital = niceToNasty($('.dropdown.hospital').val());
		specialty = niceToNasty($('.dropdown.specialty').val());
		imgURL = rotas[hospital][specialty]['img'];
		$('.rota-screenshot').attr('src', imgURL);
		$('.rota-screenshot').css("display", "block");
	}

	// Get the modal
	var modal = document.getElementById('myModal');

	// Get the image and insert it inside the modal - use its "alt" text as a caption
	var img = $('.rota-screenshot')[0];
	var modalImg = document.getElementById("img01");
	img.onclick = function(){
	    modal.style.display = "block";
	    modalImg.src = this.src;
	}

	if ($('.rota-screenshot').length === 2) {
		var img2 = $('.rota-screenshot')[1];
		var modalImg = document.getElementById("img01");
		img2.onclick = function(){
		    modal.style.display = "block";
		    modalImg.src = this.src;
		}		
	}


	// Get the <span> element that closes the modal
	var span = document.getElementsByClassName("close")[0];

	// When the user clicks on <span> (x), close the modal
	span.onclick = function() { 
	  modal.style.display = "none";
	}

	$(window).click(function() {
		if (event.target == modal) {
			modal.style.display = "none";
		}
	});

}

// if ($('#myModal2').length) {
// 	function changeImage() {
// 		hospital = niceToNasty($('.dropdown.hospital').val());
// 		specialty = niceToNasty($('.dropdown.specialty').val());
// 		imgURL = rotas[hospital][specialty]['img'];
// 		$('.rota-screenshot').attr('src', imgURL);
// 	}

// 	// Get the modal
// 	var modal = document.getElementById('myModal');

// 	// Get the image and insert it inside the modal - use its "alt" text as a caption
// 	var img = $('.rota-screenshot')[1];
// 	var modalImg = document.getElementById("img02");
// 	img.onclick = function(){
// 	    modal.style.display = "block";
// 	    modalImg.src = this.src;
// 	}

// 	// Get the <span> element that closes the modal
// 	var span = document.getElementsByClassName("close")[0];

// 	// When the user clicks on <span> (x), close the modal
// 	span.onclick = function() { 
// 	  modal.style.display = "none";
// 	}

// 	$(window).click(function() {
// 		if (event.target == modal) {
// 			modal.style.display = "none";
// 		}
// 	});

// }