$(document).ready(function(){
			changeHospitalDropdown();
			changeSpecialtyDropdown();
			changeLink();
			changeImage();
			
			$('.dropdown.hospital').on('change', changeSpecialtyDropdown);
			$('.dropdown').on('change', changeLink);
			$('.dropdown').on('change', changeImage);

})