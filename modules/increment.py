def inc(filename):

	verExt = filename.split("_")[-1]
	version = verExt.split(".")[0]
	res_str = version.replace('v', '')
	verNb =  int(res_str)
	verNb+=1
	verNb = str(verNb)
	verNb = verNb.rjust(4, '0')
	return verNb