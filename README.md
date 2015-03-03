ENG-tools beta
v. 01

by jmg*AT*phasechange*DOT*info
March 3rd 2015

To use these scripts, you will require the following:

1) An Echonest Developer account, and an API key (from https://developer.echonest.com/account/register)

2) A text file called 'apikey.txt' containing your API key, in the same folder as the scripts

3) Python 2 and the Pyen library (from https://github.com/plamere/pyen)

When you have these, proceed as follows:

1) Run 'eng_list.py' to check everything is working. Assuming it is: 

This will connect to the Echonest and generate a list of all genres (both onscreen, and as a text file in 'lists/..')
It should finish within a few seconds, and will also give you the total number of genres. 

2) A data run will require the running of 'en_genre.py'. 

This will ask how many genres to gather (currently runnong at 1370 in total), connect to the Echonest, and gather data on a maximum of 1000 artists per genre. This will be saved to 'genres/..'
It can take over 2 hours for a complete run, and will also write 'date_ratios.txt' to 'data/..' for later use. 

3) To analyse and plot the genres, start with 'eng_first.py'.

This will find the first instances of artists within the genres and writes this data to 'data/first_instances.txt'
Then run 'eng_process_firsts.py' and this will plot the results, and prodcue a graph (in 'graphs/..'). 

4) To analyse artists clustered around single start dates, rather than first instances, run 'eng_cluster.py'. 

This will ask you for a figure, the percentage of artists to be considered as a cluster. Try 5. The minimum number that will be considered, which is hardcoded, is 3 artist. 
Then run 'eng_process_clusters.py' to plot the results in 'graphs/..'

5) 'eng_cdr.py' calculates the ratio of artists with date information to those without, for each genre.

Run this, and it will use the 'data/date_ratios.txt' file from earlier. It writes the output to 'results/eng_cdr.txt'

Other features to be documented....
