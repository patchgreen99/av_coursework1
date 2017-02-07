import re, glob, os

files = sorted(glob.glob("chroma/*.jpg"))
for pathname in files:
	basename= os.path.basename(pathname)
	print basename
	# new_filename= basename[1:] + "g"
	# if new_filename != basename:
		# os.rename(
		  # pathname,
		  # os.path.join(os.path.dirname(pathname), new_filename))