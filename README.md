# MSTeams-checker
The project reads all people(who is online) in the online-conference in Microsoft Teams.

---

If you want to use this project you have to downoload those modules:
- pyscreenshot, PIL, cv2
- numpy, os, xlutils
- pyautogui, xlrd, excel2img
- pytesseract

And you also need monitor 1920x1080!

---

How to start:
- You have to downoload all needed modules.
- You have to downoload all files from this repository in the folder, but do not 
change names of files and do not replace files or folders (it can break launching of the programm)
- Next you have to create excel-files with rules for creating it (check rules in 
in the 'README.txt' in the 'TablesOfGroups' folder.
- Next you have open 'ColledgeGroups.py' and create there lists for groups of 
students that you want to scan. For example 'first_group = []' and fill it with 
full names like you writed them in Excel-files (with the same rules). 
There are already 2 groups and 1 group of teachers, you can delete it if 
you want.
- In files 'Handler.py' and 'CropingPhotos' you have to choose your way to pytesseract.
You can do it by writing this 'pytesseract.pytesseract.tesseract_cmd = way'
- Next go to 'Handler.py' and move to 30th line. There you have to create readbook and 
workbook for each Excel-file in 'TablesOfGroups'. Use the code like the example.
- Next go to 'Handler.py' again and move to 76th line: there you have to compare 
the full name of the student with groups and if this student is in that group 
then write him name in the excel-file of his group. ( you can remove some 
unnecessary comparisons if you do not need them. ). There are also cycles 
in comparisons with 'strange' range (25 and 27). Do not worry, write there 
a number of people in the group of comparison. For example: 
if you have 25 people in group, so write number 25 in the range of cycle.
- If you have done all right, you have to open MS Teams in the conference, zoom it 
interface to 145% and open participants tab (do not leaf down), 
now you have to launch 'Main.py' and wait for the end of working.
- Go to folder 'Result' and collect results.
WARNING - !Do not overlap the participants area with other windows!

---

I understand that it is hard to launch this project, sorry, i am just learning.
If you can commit my code to the better code, i would be very pleased.
