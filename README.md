# Windows_Programming_Final
## The final project of windows programming cource~

執行方式：同時執行 running.py , camera.py




###進度：
flag is in the flag.npy
	if flag != 0
		1. do labeling
			a. creeate 16 directory
			b. open text file to record the filename
			c. create file with name record in text file
		2. calculate accuracy
			a. if result != flag then print no else yes
			b. record in the text file named acc.txt
		3. statistic
			create confusion 2d-array 
	else 
		print(numpy.argmax(result))
