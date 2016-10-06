ENG-Tools beta v. 12

by J. M. Gagen
jmg*AT*phasechange*DOT*info
j*DOT*gagen*AT*gold*DOT*ac*DOT*uk

www*DOT*phasechange*DOT*info

October 6th 2016

These scripts have been created to facilitate research into musical genre using the Echonest. 
They acquire data from the Echonest (via the API), process it, and facilitate statistical and network analysis.  

This is research software; USE IT AT YOUR OWN RISK. 
I will respond to emails if possible, BUT THIS SOFTWARE HAS NO FORMAL SUPPORT.

LICENCE: 
http://creativecommons.org/licenses/by-nc-sa/3.0/


/////////////////////////////////////////////////////////////////////////
N.B. The Echonest API ceased to function on May 31st 2016. The provision of new API keys has already ceased. 
The Spotify Web API will be taking over the role of the EN API. 
Full announcement at http://http://developer.echonest.com/
Given this, I have included a .ZIP file containing a dataset from April 9th 2016 within this repository. 
/////////////////////////////////////////////////////////////////////////

LATEST CHANGES AND ADDITIONS: 

- New version of 'nhm' (b05) deals with time-sliced data.

- New version of 'eng_network_single' (b24) deals with time-sliced data.

- New version of 'eng_nodesets' (b06) deals with artist time-slice data (written by 'timeslicer')

- 'timeslicer' deals with raw genre files and writes new ones after artist time-slicing.

- Updated 'ghp_..py' to handle multiple gexf inputs. 

- Added 'eng_en_mb_map' to generate a text file containing EchoNest-to-MusicBrainz artist IDs to facilitate mapping.

- Updated 'ghp_..py' (to facilitate like-for-like node placement upon hive-axes across eras). 

- Updated 'JG' method version of 'nhm_b' to 'nhm_b03.py' (to incorporate maximum node-hybridity values and 'artist-uniques' totals).

- Added 'ghp_..py' to facilitate hive plots. 

- Updated 'en_genre' (and associated scripts) to grab and deal with EchoNest IDs. This will facilitate later mapping to MusicBrainz IDs. 

- Added 'genres_2016_04_09.zip' to facilitate analysis once the Echo Nest API has shut down. 


REQUIREMENTS 

To use ENG-Tools you will require the following:

1) An Echonest Developer account, and an API key (from https://developer.echonest.com/account/register)

2) A text file called 'apikey.txt' containing your Echonest API key, in a 'config/..' subfolder (i.e. 'config/apikey.txt' within the main ENG-Tools folder). 

/////////////////////////////////////////////////////////////////////////
N.B. The Echonest API ceased to function on May 31st 2016. The provision of new API keys has already ceased. 
The Spotify Web API will be taking over the role of the EN API. 
Full announcement at http://http://developer.echonest.com/
Given this, I have included a .ZIP file containing a dataset from April 9th 2016 within this repository. 
/////////////////////////////////////////////////////////////////////////

3) Python 2.7, the 'pyen' library (from https://github.com/plamere/pyen), the 'matplotlib' library (from http://matplotlib.org), the 'scipy' library (from http://www.scipy.org), and the 'networkx' library (from https://networkx.github.io/). 
It is likely that the 'community' library (https://bitbucket.org/taynaud/python-louvain) will be used in later versions.  


USAGE 

DATA ACQUISITION

1) eng_list:

This script connects to the Echonest and generate a directory ('lists/..') and a list of all genres (both onscreen, and as a text file in 'lists/..'). 
It usually takes a few seconds, and will give you the total number of genres. 

/////////////////////////////////////////////////////////////////////////
This data can now be found in 'genres_2016_04_09.zip'
Unzip so a 'genres' folder appears as a subdirectory in the main folder.
/////////////////////////////////////////////////////////////////////////

2) en_genre: 

This will ask how many genres to gather (currently returning 1383 in total), connect to the Echonest, and gather data on a maximum of 1000 artists per genre. 
This will be saved to 'genres/..' (a directory generated by the script) as a series of text files, one per genre. 
It can take over 2 hours for a complete run, and will also write 'data/date_ratios.txt' for later use. 

/////////////////////////////////////////////////////////////////////////
This data can now be found in 'genres_2016_04_09.zip'
Unzip so a 'genres' folder appears as a subdirectory in the main folder.
/////////////////////////////////////////////////////////////////////////


DATA PROCESSING AND ANALYSIS

1) eng_first:

To analyse and plot the genres, start with 'eng_first.py'. 
This will find the first instances of artists within the genres and writes this data to 'data/first_instances.txt'

2) eng_cluster: 

To analyse artists clustered around single start dates, rather than first instances, run 'eng_cluster.py'. 
This will ask you for a figure; either an absolute value or percentage of artists to be considered as a cluster. 
The minimum number of artists that will be considered a cluster, is 2; this is hardcoded. 
If you choose a percentage that works out at less than 2, the figure is set as to 2. 

3) eng_cdr: 

This calculates the ratio of artists with date information to those without, for each genre. 

Run this, and it will use the 'data/date_ratios.txt' file from earlier. It writes the output to 'results/eng_cdr.txt'

4) eng_fam_hot: 

'eng_fam_hot.py' calculates the lowest, highest and average 'Familiarity' and 'Hotttnesss' metrics for each genre and stores these in 'results/'.  

5) eng_prob.py:

'eng_prob.py' converts the output from a single genre plot (the results file from 'eng_plot.py'- a genre data file which has been converted to a frequency distribution) to a probability distribution. 
The purpose of this is to facilitate analysis at a later date. To use this script, copy a single-genre plot file to 'data/..' and rename it to 'genre_freq_data.txt'. 

6) eng_en_mb_map: 

'eng_en_mb_map..py' reads all genre files and generates a text file with 'Artist Name ^ EchoNest ID ^ MusicBrainz ID' (to facilitate mapping EN to MB)


NETWORK CREATION AND ANALYSIS

1) timeslicer: 

This generates an OMEGAYEAR folder in 'data/', with associated timesliced genre files (in 'data/OMEGAYEAR/genres') and 'data/OMEGAYEAR/OMEGAYEAR_artistNums.txt'.
It is designed to allow timesliced-data processing using existing methods.

2) eng_nodesets: 

This converts the genres to set()s containing 'artists' as elements. It then finds all intersections based upon shared artists. 
The output file from this ('data/wuGraph_data.txt') is a weighted undirected edgelist for use by 'eng_network_multi' and 'eng_network_single'.  

3) eng_network_multi: 

'eng_network_multi' processes and renders networks for all dates in the 'first_clusters' file, and outputs, among other things, nodelists, edgelists, GEXF files, Laplacian Spectra, and other analyses and results. 
Network layout parameters can be edited in 'config/config_nw.txt'. 

4) eng_network_single: 

This generates a single network based upon user input, and outputs analysis to 'results/analysis' file and pagerank to 'data/pagerank.txt' file. 

5) pr_process: 

'pr_process' reformats 'data/pagerank.txt' and outputs 'results/pr_results.txt'. 

6) pr_hot_fam_process: 

'pr_hot_fam_process' grabs info from 'results/pr_results.txt' and 'results/eng_fam_hot__data.txt', and writes 'results/pr_hot_fam_results.txt'. 


HYBRIDITY METRICS

1) nhm: 

Run 'nhm.py' to calculate the Network Hybridity Metric (NHM) for all graphs (based upon the presence of 'gexf/directed/OMEGAYEAR.gexf' files). 
'nhm.py' also outputs 'data/nhm_plot.txt'. THIS WILL THROW AN ERROR IF NO .GEXF FILES ARE FOUND.


PLOTTERS

1) eng_process_firsts:

Run 'eng_process_firsts.py' to plot the results from 'eng_first.py', and produce a graph (in 'graphs/..'). 

2) eng_process_clusters:

Run 'eng_process_clusters.py' to plot the results from 'eng_clusters.py' (in 'graphs/..'). 

3) eng_multi_plot: 

To plot the graph for artists-over-time for each and every genre, run 'eng_multi_plot.py'. 
It will produce one graph (named with the version number and genre) for each genre file (and place them in 'graphs/..'). 
Individual genres can easily be plotted in two ways; either run 'eng_multi_plot' having placed only one genre file in the 'genres/..' folder, or run 'eng_plot.py'. 
If doing the later, you will need to copy a genre data file and place it in 'data/..'. Then rename it to 'genre_2_plot.txt'. 
Also, 'eng_plot' and 'eng_multi_plot' have statistical calulations integrated into them; these are written to 'results/eng_multi_plot_stats_data.txt'. 

4) eng_plot_retromatic:

'eng_plot_retromatic.py' plots the data gleaned (manually) from 'http://everynoise.com/retromatic.html'. 
This charts the genres of the most popular 5000 songs for every year since 1950 (based on Echonest 'song' genres figures; these are unavailable to the API). 
A file containing this data can be found in the 'data/..' directory, and this is where the script will look for 'retromatic.txt'.

5) eng_plot_artists:

'eng_plot_artists.py' uses the file ouput by ‘eng_multi_plot’ (moved to ‘data/..’ and renamed as ‘eng_multi_plot_data.txt’) to calculate and plot the inception dates of all artists over time, regardless of genre. 

6) pr_plotter: 

'pr_plotter' takes 'results/pr_hot_fam_results.txt' and plots 3 graphs from this (PageRank-Mean Familiarity, PageRank-Mean Hotttnesss, and Mean Hotttness-Mean Familiarity). 

7) nhm_plotter: 

Run 'nhm_plotter.py' after 'nhm.py' to plot 2 graphs (in 'graphs/..'). 
One shows 'Hgraph' (solid red) and 'Mean-Hnode' (dashed blue). 
The other shows '% Hnode = 0.5 hybrid nodes' (solid red), '% Progenitor nodes' (dashed blue), and '% Sink nodes' (dotted black). 

8) ghp: 

'ghp...py' reads gexf files in 'gexf/directed' and plots SVG hives (in 'networks/hives/all')


MANIFEST 

(1) en_genre.py

(2) eng_cdr.py

(3) eng_cluster.py

(4) eng_first.py

(5) eng_fam_hot.py

(6) eng_list.py

(7) eng_multi_plot.py

(8) eng_plot.py

(9) eng_plot_artists.py

(10) eng_plot_retromatic.py

(11) eng_prob.py

(12) eng_process_clusters.py

(13) eng_process_firsts.py

(14) eng_nodesets.py

(15) eng_network_multi.py

(16) eng_network_single.py

(17) pr_process.py

(18) pr_hot_fam_process.py

(19) pr_plotter.py

(20) nhm_...cr.py (CR method)

(21) nhm.py (JG method)

(22) nhm_plotter.py

(23) ghp.py

(24) eng_en_mb_map.py

(25) timeslicer.py

(26) config/config_nw.txt (Network layout config. file)

(27) data/retromatic.txt

(28) data/date_ratios.txt

(29) genres_2016_04_09.zip

(30) config/apikey.txt (BLANK - REQUIRES API KEY) - DEPRECATED