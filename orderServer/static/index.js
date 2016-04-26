function plusValue(itemID) {
	cur = document.getElementById("Order-item-"+itemID.toString()).value;
	document.getElementById("Order-item-"+itemID.toString()).value = parseInt(cur)+1
}

function minusValue(itemID) {
	cur = document.getElementById("Order-item-"+itemID.toString()).value;
	if ( cur != "0" ) {
		document.getElementById("Order-item-"+itemID.toString()).value = parseInt(cur)-1
	}
}
