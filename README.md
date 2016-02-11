ENG-Tools beta v. 09

by J. M. Gagen
jmg*AT*phasechange*DOT*info

http://www*DOT*phasechange*DOT*info

February 11th 2016

These scripts have been created to facilitate research into musical genre using the Echonest. 
They acquire data from the Echonest (via the API), process it, and facilitate statistical and network analysis.  

This is research software; USE IT AT YOUR OWN RISK. 
I will respond to emails if possible, BUT THIS SOFTWARE HAS NO FORMAL SUPPORT.


LICENCE: 

http://creativecommons.org/licenses/by-nc-sa/3.0/


LATEST ADDITIONS: 

- 'shm' calculates the Simple Hybridity Metric (SHM) for nodes and graphs. 

- 'eng_network_wd' calculates 'artist Total' for networks. 

- 'eng_network_wd' renders undirected network AFTER directing to help calculate final characteristics.  

- 'eng_network_wd' removes edges where, in a directed network, the nodes have the same inception date. 

- 'eng_network_wd' can optionally remove nodes based upon inception date. 

- 'en_genre' removes empty genres from 'date_ratios.txt'

- 'eng_cdr' generates 'data\artistNums.txt' for use (later) by 'eng_network_wd.py'

- 'eng_network_wd' can optionally remove self-loops and zero-degree nodes.

- 'eng_network_wd' adds genre start dates and generates directed graph GEXF file.

- 'eng_cluster' updated to accept absolute artist numbers (as well as %)

- 'config_nw.txt' configures network layout. 

- 'eng_network_wd' takes 'eng_nodesets' weighted edgelist and plots undirected and directed networks. 

- 'eng_fam' added, to calculate hi, low and average `familiarity' ratings for genres

- 'en_genre' deletes empty genre files automatically

- 'eng_nodesets' script converts genres into set()s and finds intersections

- 'en_genre' now captures artists' musicbrainz ID (and discards those without)

A full manifest can be found at the end of this readme file. 


REQUIREMENTS: 

To use ENG-Tools you will require the following:

1) An Echonest Developer account, and an API key (from https://developer.echonest.com/account/register)

2) A text file called 'apikey.txt' containing your Echonest API key, in the same folder as the scripts

3) Python 2.7, the 'pyen' library (from https://github.com/plamere/pyen), the 'matplotlib' library (from http://matplotlib.org), the 'scipy' library (from http://www.scipy.org), and the 'networkx' library (from https://networkx.github.io/). It is likely that the 'community' library (https://bitbucket.org/taynaud/python-louvain) and the 'igraph' library will be used in later versions; the Python version of iGraph can be obtained from http://igraph.org/python/ 

USAGE: 

1) Run 'eng_list.py'. 

This script will connect to the Echonest and generate a directory ('lists/') and a list of all genres (both onscreen, and as a text file in 'lists/'). It should finish within a few seconds, and will give you the total number of genres. 

2) A data run will require the running of 'en_genre.py'. 

This will ask how many genres to gather (currently returning 1379 in total), connect to the Echonest, and gather data on a maximum of 1000 artists per genre. This will be saved to 'genres/' ( a directory generated by the sript) as a series of text files, one per genre. It can take over 2 hours for a complete run, and will also write 'date_ratios.txt' to 'data/' for later use. 

3) To analyse and plot the genres, start with 'eng_first.py'.

This will find the first instances of artists within the genres and writes this data to 'data/first_instances.txt'
Then run 'eng_process_firsts.py' and this will plot the results, and produce a graph (in 'graphs/'). 

4) To analyse artists clustered around single start dates, rather than first instances, run 'eng_cluster.py'. 

This will ask you for a figure, the percentage of artists to be considered as a cluster. 5%, for example. The minimum number of artists that will be considered a cluster, is 3; this is hardcoded. If you choose a percentage that works out at less than 3, the figure is set as to 3. Then run 'eng_process_clusters.py' to plot the results (in 'graphs/'). 

5) To plot the graph for artists-over-time for each and every genre, run 'eng_multi_plot.py'. It will produce one graph (named with the version number and genre) for each genre file (and place them in 'graphs/'). A full set of plots takes around 6 minutes with an i5 processor. Individual genres can easily be plotted in two ways; either run 'eng_multi_plot' having placed only one genre file in the 'genres/' folder, or run 'eng_plot.py'. If doing the later, you will need to copy a genre data file and place it in 'data/'. Then rename it to 'genre_2_plot.txt'. 'eng_plot' and 'eng_multi_plot' now have statistical calulations integrated into them; these are written to 'results/eng_multi_plot_stats_data.txt'. 

6) 'eng_cdr.py' calculates the ratio of artists with date information to those without, for each genre.
Run this, and it will use the 'data/date_ratios.txt' file from earlier. It writes the output to 'results/eng_cdr.txt'

7) 'eng_hot.py' calculates the lowest, highest and average 'Hotttnesss' metrics for each genre and stores this in 'results/'. 

8) 'eng_fam.py' calculates the lowest, highest and average 'Familiarity' metrics for each genre and stores this in 'results/'. 

9) 'eng_prob.py' converts the output from a single genre plot (the results file from 'eng_plot.py'- a genre data file which has been converted to a frequency distribution) to a probability distribution. The purpose of this is to facilitate analysis at a later date. To use this script, copy a genre plot file to 'data/' and rename it to 'genre_freq_data.txt'. 

10) 'eng_plot_retromatic.py' plots the data gleaned (manually) from 'http://everynoise.com/retromatic.html' This charts the genres of the most popular 5000 songs for every year since 1950 (based on Echonest 'song' genres figures; these are unavailable to the API). A file containg this data can be found in the 'data/' directory, and this is where the script will look for 'retromatic.txt'.

11) 'eng_plot_artists' uses the file ouput by ‘eng multi plot’ (moved to ‘data/’ and renamed as ‘eng multi plot data.txt’) to calculate and plot the inception dates of all artists over time, regardless of genre. 

12) 'eng_nodesets' converts the genres to set()s containing 'artists' as elements. It then finds all intersections based upon shared artists. 

13) The output file from this ('wuGraph_data') can then be processed with 'eng_network_wd'. This outputs, among other things, GEXF files, Laplacian Spectra, and other analyses and results. 

14) Network layout parameters can be edited in 'config_nw.txt'. 

15) Rename a GEXF file ('gexf/shm.gexf') and run 'shm.py' to calculate the SimpleHybridity Metric (SHM) for a graph. 


MANIFEST: 

(1) en_genre.py

(2) eng_cdr.py

(3) eng_cluster.py

(4) eng_first.py

(5) eng_hot.py

(6) eng_list.py

(7) eng_multi_plot.py

(8) eng_plot.py

(9) eng_plot_artists.py

(10) eng_plot_retromatic.py

(11) eng_prob.py

(12) eng_process_clusters.py

(13) eng_process_firsts.py

(14) eng_nodesets.py

(15) eng_fam.py

(16) eng_network_wd.py

(17) shm.py

(18) apikey.txt (BLANK - REQUIRES API KEY)

(19) config_nw.txt
