# Doug’s Fancy CSV file seperator
#### Video Demo: https://youtu.be/qGR9nLj5Two
#### Description:

This project is for my final in Harvard cs50 online course.  The purpose is to gather a csv file from a user (web based).  Take that file and split it into 3 different files, good, bad and summery.   
This originated from a friend that works for a utility company that has the highest standards of energy management. In the fall of 2017, AWMS, Inc., a third-party certification body, conducted an ISO 50001 and Superior Energy Performance audit of Des Moines Water Works’ energy management system and subsequent improved energy performance. Des Moines Water Works is the only water utility in the world to be ISO 50001 registered and certified as to Superior Energy Performance® 50001 and recognized by the DOE at the Gold level.  Des Moines Water Works joins companies like Volvo, Cummins and 3M as energy management leaders in the U.S.
As part of this standard they recieve data from Verizon Connect.  This data tracks their fleet of trucks.  It includes data like, start time, run time, idle time, number of stops, etc.  
While this data is invaluable to them in their certification audits and tracking of how well they are "performing" it was riddled w/ bad data.  Oftentimes unusable.  I wanted to build them a web app. where they could upload these csv files and we could programmatically remove all the data they deemed bad (no start time, end time, etc).  I then wanted to split the file into a good and bad file.  These files would then be available for them to immediately download.
In addition to removing the bad data, we wanted to summarize the hundreds of lines of data they were getting and create yet another file.  This one gets the running time of every vehicle and driver, totals them up and gives them an idle time percentage where they can track performance for each employee and truck.  
This program has turned an all day affair into a click of a few buttons.  Saving them countless hours yearly.  

 


