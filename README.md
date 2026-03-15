I didn't really know what to do so I decided to make an app that tracks partial credit scores for 112 students, 
including their submissions for the problems. This is meant to be run in Google Colab with the right folder setup in your drive
It compiles their solutions adds all of the corrected and uncorrected solutions from a folder in the same parent folder with the structure:
/original-ws{num}/Version {letter}/{problemName}/{andrewID}-ws{num}-{problemName}.py, and a sheet with the andrewID in a column and
a concatenated string of problem and then version as the header in each column to the right of that one. It has functions to write this
to the database, and has functions to add their partial credit scores as well. It obviously creates the database, it updates
the database when a student submits new partial credit code and the script is rerun. It reads the data to go through and write
the scores and comments to a Google sheet. It also has a menu where you can go through and delete specific student submissions (in the case
of an AIV, student request, or other special case), this is done by searching by andrewID first and then narrowing down to the specific problem.
It finishes off its functionality by allowing the user to export this data to a sheet (but only students that have partial credit submissions).
The actual comparison code is left out because it's not mine and not public. You can assume it's in another cell and can be called when needed
