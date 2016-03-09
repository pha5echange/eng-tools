ENG-Tools beta v. 11.4

by J. M. Gagen
jmg*AT*phasechange*DOT*info

http://www*DOT*phasechange*DOT*info

March 7th 2016

These scripts have been created to facilitate research into musical genre using the Echonest. 
They acquire data from the Echonest (via the API), process it, and facilitate statistical and network analysis.  

This is research software; USE IT AT YOUR OWN RISK. 
I will respond to emails if possible, BUT THIS SOFTWARE HAS NO FORMAL SUPPORT.


LICENCE: 

http://creativecommons.org/licenses/by-nc-sa/3.0/


LATEST CHANGES AND ADDITIONS: 

- Added check for 'Directed Acyclic Graph' to 'eng_network_wd' and 'eng_network_wd...a'

- Added 'pr_plotter' to plot and output PageRank-Mean Familiarity, PageRank-Mean Hotttnesss, and Mean Hotttness-Mean Familiarity. 

- Added 'pr_hot_fam_process' to write a datafile containing genre, pagerank, mean familiarity and mean hotttnesss. 

- Added 'pr_process_a01.py' to reformat Page Rank data from 'eng_network_wd...a.py'

- 'en_genre' and 'eng_list' now replace spaces in genre names with underscores (to note presence of spaces).

- Single-network version of 'eng_network_wd' now has an 'a' after the version number and incorporates 'Page Rank'.

- Updated 'nhm_plotter' to output '.eps' files, and label plots. 

- 'SHM' script and plotter script updated and renamed to 'NHM' (Network Hybridity Metric)

- Subfolder 'gexf/directed/' added to folder structure. 

- 'eng_multiplot' saves images to 'graphs/multi/'. 

- 'eng_fam' and 'eng_hot' combined into one script ('eng_fam_hot'). 

- 'eng_network_wd' makes networks for all `first_clusters'. 

- 'shm' now looks for 'OMEGAYEAR.gexf' files in 'gexf/..' and calculates for all. 

- 'gexf/directed/*.gexf' examples added to prevent 'nhm' errors. 

- 'eng_network_wd' now outputs 'gexf/directed/OMEGAYEAR.gexf' file for directed graphs. 

- 'shm_h_plotter' now outputs 2 graphs, each with 2 lines ('GraphH' + 'meanNodeH' and '% H=1.0' + '% Progenitors') 

- 'shm_H_plotter' makes simple line-graphs of SHM results.

- 'shm' saves log, results and 'nodes' files, and 'shm_plot' file for use by 'shm_H_plotter'. 

- 'shm' calculates the Simple Hybridity Metric (SHM) for nodes and graphs. 

A full manifest can be found at the end of this readme file. 


REQUIREMENTS: 

To use ENG-Tools you will require the following:

1) An Echonest Developer account, and an API key (from https://developer.echonest.com/account/register)

2) A text file called 'apikey.txt' containing your Echonest API key, in a 'config/..' subfolder (i.e. 'config/apikey.txt' within the main ENG-Tools folder). 

3) Python 2.7, the 'pyen' library (from https://github.com/plamere/pyen), the 'matplotlib' library (from http://matplotlib.org), the 'scipy' library (from http://www.scipy.org), and the 'networkx' library (from https://networkx.github.io/). It is likely that the 'community' library (https://bitbucket.org/taynaud/python-louvain) and the 'igraph' library will be used in later versions; the Python version of iGraph can be obtained from http://igraph.org/python/ 

USAGE: 

1) Run 'eng_list.py'. 

This script will connect to the Echonest and generate a directory ('lists/..') and a list of all genres (both onscreen, and as a text file in 'lists/'). It should finish within a few seconds, and will give you the total number of genres. 

2) A data run will require the running of 'en_genre.py'. 

This will ask how many genres to gather (currently returning 1383 in total), connect to the Echonest, and gather data on a maximum of 1000 artists per genre. This will be saved to 'genres/..' ( a directory generated by the script) as a series of text files, one per genre. It can take over 2 hours for a complete run, and will also write 'data/date_ratios.txt' for later use. 

3) To analyse and plot the genres, start with 'eng_first.py'.

This will find the first instances of artists within the genres and writes this data to 'data/first_instances.txt'
Then run 'eng_process_firsts.py' and this will plot the results, and produce a graph (in 'graphs/..'). 

4) To analyse artists clustered around single start dates, rather than first instances, run 'eng_cluster.py'. 

This will ask you for a figure; either an absolute value or percentage of artists to be considered as a cluster. The minimum number of artists that will be considered a cluster, is 3; this is hardcoded. If you choose a percentage that works out at less than 3, the figure is set as to 3. Then run 'eng_process_clusters.py' to plot the results (in 'graphs/..'). 

5) To plot the graph for artists-over-time for each and every genre, run 'eng_multi_plot.py'. It will produce one graph (named with the version number and genre) for each genre file (and place them in 'graphs/..'). A full set of plots takes around 6 minutes with an i5 processor. Individual genres can easily be plotted in two ways; either run 'eng_multi_plot' having placed only one genre file in the 'genres/..' folder, or run 'eng_plot.py'. If doing the later, you will need to copy a genre data file and place it in 'data/..'. Then rename it to 'genre_2_plot.txt'. Also, 'eng_plot' and 'eng_multi_plot' have statistical calulations integrated into them; these are written to 'results/eng_multi_plot_stats_data.txt'. 

6) 'eng_cdr.py' calculates the ratio of artists with date information to those without, for each genre.
Run this, and it will use the 'data/date_ratios.txt' file from earlier. It writes the output to 'results/eng_cdr.txt'

7) 'eng_fam_hot.py' calculates the lowest, highest and average 'Familiarity' and 'Hotttnesss' metrics for each genre and stores these (as 2 files) in 'results/'.  

8) 'eng_prob.py' converts the output from a single genre plot (the results file from 'eng_plot.py'- a genre data file which has been converted to a frequency distribution) to a probability distribution. The purpose of this is to facilitate analysis at a later date. To use this script, copy a genre plot file to 'data/..' and rename it to 'genre_freq_data.txt'. 

9) 'eng_plot_retromatic.py' plots the data gleaned (manually) from 'http://everynoise.com/retromatic.html' This charts the genres of the most popular 5000 songs for every year since 1950 (based on Echonest 'song' genres figures; these are unavailable to the API). A file containing this data can be found in the 'data/..' directory, and this is where the script will look for 'retromatic.txt'.

10) 'eng_plot_artists.py' uses the file ouput by ‘eng_multi_plot’ (moved to ‘data/..’ and renamed as ‘eng_multi_plot_data.txt’) to calculate and plot the inception dates of all artists over time, regardless of genre. 

11) 'eng_nodesets' converts the genres to set()s containing 'artists' as elements. It then finds all intersections based upon shared artists. The output file from this ('data/wuGraph_data.txt') is a weighted undirected edgelist for use by... 

12) 'eng_network_wd' processes and renders networks for all 'first_clusters' genres, and outputs, among other things, nodelists, edgelists, GEXF files, Laplacian Spectra, and other analyses and results. Network layout parameters can be edited in 'config/config_nw.txt'. 

13) 'eng_network_wd_...a' generates single network based upon user input, and outputs analysis to 'results/analysis' file and  pagerank to 'data/pagerank.txt' file. 

14) 'pr_process' reformats 'data/pagerank.txt' and outputs 'results/pr_results.txt'. 

15) 'pr_hot_fam_process' grabs info from 'results/pr_results.txt' and 'results/eng_fam_hot__data.txt', and writes 'results/pr_hot_fam_results.txt'. 

16) 'pr_plotter' takes 'results/pr_hot_fam_results.txt' and plots 3 graphs from this (PageRank-Mean Familiarity, PageRank-Mean Hotttnesss, and Mean Hotttness-Mean Familiarity). 

17) Run 'nhm.py' to calculate the Network Hybridity Metric (NHM) for all graphs (based upon the presence of 'gexf/directed/OMEGAYEAR.gexf' files). 'nhm.py' also outputs 'data/nhm_plot.txt'.

18) Run nhm_plotter.py' after 'nhm.py' to plot 2 linegraphs (in 'graphs/..'). One shows 'GraphH' (dashed blue) and 'Mean-NodeH' (solid red). The other shows '% H=1.0 hybrid nodes' (dashed blue) and '% Progenitor nodes' (solid red). 


MANIFEST: 

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

(15) eng_network_wd.py

(16) eng_network_wd_...a.py

(17) pr_process_a01.py

(18) pr_hot_fam_process.py

(19) pr_plotter.py

(20) nhm.py

(21) nhm_plotter.py

(22) config/apikey.txt (BLANK - REQUIRES API KEY)

(23) config/config_nw.txt (Network layout config. file)

(24) data/retromatic.txt

(25) Multiple example '.gexf' files added to gexf/directed/
