def getName(filename):

	name = filename.split("_")
	del name[-1]
	name = '_'.join(name)
	return name