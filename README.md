# T-Drive trajectory data analysis
T-Drive trajectory data sample exploratory analysis


Requirements:

1) Made use of Folium, Numpy, Pandas, GeoPandas, IPython, Jupyter, NetworkX, Scikit-Learn, (Selenium)
2) pip freeze -l > requirements.txt




Notebooks:

Notebooks assume that the initial data is in folder "data." Processed data is put in folder "processed_data", so need to create it as well.

1) 01_tdrive_data_loading - Just loading data and transforming it into a pickle
2) 02_initial_exploration - First look at the dataset. Some plotting, getting used to Folium, etc
3) 03_data_preprocessing - Removing points outside Beijing, Removing duplicate rows, Filtering points by speed, Resampling frequency.
4) 04_second_exploration - Using processed data look at taxis activity through time dimension, find most active hours, avg moved distance, distribution of distances covered, etc.
5) 05_spatial_tessellations - Create rectangular spatial tessellations. Visualize counts of taxis through time.
6) 06_transitions - Using tessellations and PageRank algorithm, find the most important places in Beijing.
7) 07_machine_learning - Some attempt at applying machine learning, but not too deep :) Create linear models and take a brief look at coefficients that affect counts in some tiles of Beijing.


All html versions of the notebooks are in the folder notebooks_html.


Some more interesting results are in .gif files in the same folder as notebooks.

1) monday.gif - how count of taxis change in grid during day
2) monday_active.gif - how count of active taxis (found with a simple heuristic) change through time
3) monday_pagerank.gif - shows what kind of transitions are most popular ones. Which are more popular tiles throughout the day




