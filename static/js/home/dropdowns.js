function changeLink() {
	// Change go button 
	var hospital = niceToNasty($('.dropdown.hospital').val());
	var specialty = niceToNasty($('.dropdown.specialty').val());
	var link = `upload/${hospital}/${specialty}`;
	$('.upload-page-form').attr('action', '/nhsrotaconverter/' + link);
}

function changeHospitalDropdown() {
// Set hospital dropdown values based on what's in the rotas object
	
	// Makes list empty
	$('.dropdown.hospital')[0].length = 0;
	
	// Makes an array of options
	var options = Object.keys(rotas);

	// Turns the options into nice names
	options = options.map(x => nastyToNice(x));
	console.log(options);

	// Turns the nice names into an array of option elements
	options = options.map(o => $(`<option> ${o} </option>`) );
	
	// Adds the option elements to the dropdown select element
	$('.dropdown.hospital').append(options);
}

function changeSpecialtyDropdown() {
// Change specialty dropdown based on hospital dropdown value
	
	// Makes list empty
	$('.dropdown.specialty')[0].length = 0;

	// Gets the value of the hospital dropdown nice name
	var hospitalNiceName = $('.dropdown.hospital').val(); 

	// Gets the NON nice name from the hospital nice name
	var hospital = niceToNasty(hospitalNiceName);

	// Gets the specialties array from the hospital
	var options = Object.keys(rotas[hospital]);

	// Turns the specialties array into an array of nice names
	options = options.map(x => nastyToNice(x));
	
	// Turns the nice names array into an array of option elements
	options = options.map(o => $(`<option> ${o} </option>`) );
	
	// Adds the option elements to the dropdown select element
	$('.dropdown.specialty').append(options);
}
