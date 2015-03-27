SETUP FOR IMAGE PROCESSING

1. Folders you should already have in the directory you are analyzing:
	A. "PNGs": Contains files for each round of videoing. Those files each contain the PNGs to be sorted.
	B. "Prep data": Contains all the files describing the location of the arenas and objects
	C. "Sorted images": Will be filled with the folders of sorted images

2. Files you should already have in the directory you are analyzing:
	A. PNGs: Located within the folders within the "PNGs" folder. Should already be limited so that they start at the beginning of exploration in arena 1 and end with the end of exploration in arena 4.
	B. "XX_results.csv": Located within the "Prep data" folder. Should have one of these files per round of videoing. See "File setup" directions below.
	C. "criteria.csv": Located within the "Prep data" folder. Contains both the inclusion (animal is close to object) and exclusion (animal is on top of object) areas around the center of each object.

3. File setup:
	A. "XX_results.csv": Rows (0 to (# of arenas*2)), columns 0 to 2 - Data from FIJI noting the center of object A and object B (in that order), in order by arena.
			     Rows (1+(# of arenas*2) to 2*(# of arenas*2)), columns 0 to 2 - data from FIJI noting the location of two opposite corners for each arena, in order by arena. It doesn't matter which corners are selected or the order in which they are selected, so long as they are opposite one-another.
			     Rows (1 to # of arenas), columns 3 to 5 - In column 3, the list of the animals (a.k.a. arenas) active in this video. In the adjoining column for each, the video frame at which exploration starts. In row 1, column 5, the total number of frames for that recording period (e.g. 8991 for 5 minutes).
	B. "criteria.csv": Assumes that the inclusion (animal near object) and exclusion (animal on top of object) areas around each object are the same.
			   Rows 0-3, column 1 - In order, inclusion width radius for A and B, inclusion height radius for A and B, exclusion width radius for A and B, exclusion height radius for A and B.