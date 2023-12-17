def version_increment(version):
	"""
	Function to Increment version number.
	
	Logic:
		Delete "v" to isolate number. 
		Increment number and add padding.
		Add "v" before the incremented number to make the incremented verion.

	Args:
		version (str):  input version to increment, format : v0000
	
	Return:
		incremented_version (str): output incremented version, format : v0000
	"""

	version_number = version.replace('v', '')
	version_number =  int(version_number)
	version_number+= 1
	version_number = str(version_number)
	version_number = version_number.rjust(4, '0')
	incremented_version = f"v{version_number}"
	return incremented_version