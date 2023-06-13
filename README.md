# Datasets-of-AIS-Trajectories-from-Danish-Waters
Public filtered data sets of AIS Trajectories from Danish Waters. Data sets vary in ROI size, time period, included ship types ect. Some data sets may be annotated with abnormal behavior.

Using Deep Learning for detection of maritime abnormal behaviour in spatio temporal trajectories is a relatively new and promising application. Open access to the Automatic Identification System (AIS) has made large amounts of maritime trajectories publically available. However, these trajectories are unannotated when it comes to the detection of abnormal behaviour. 
The lack of annotated datasets for abnormality detection on maritime trajectories makes it difficult to evaluate and compare suggested models quantitatively. With this dataset, we attempt to provide a way for researchers to evaluate and compare performance.  

We have manually labelled trajectories which showcase abnormal behaviour following an collision accident. The annotated dataset consists of 521 data points with 25 abnormal trajectories. The abnormal trajectories cover among other; Colliding vessels, vessels engaged in Search-and-Rescue activities, law enforcement, and commercial maritime traffic forced to deviate from the normal course  

This repository provides ustility functions for a collection of datasets AIS Trajectories from Danish Waters. 
One dataset consists of unlabelled trajectories for the purpose of training unsupervised models. This dataset can be considered representative of normal maritime traffic during the collection period. The normal traffic in the ROI has a fairly high seasonality related to fishing and leisure sailing traffic. 
The other dataset consists of a total of 521 trajectories of which 25 is labelled as abnormal for the purpose of evaluation. The labelled dataset is an example of a SAR event and cannot not be considered representative of a large population of all SAR events. The remaining normal traffic in the labelled dataset is representative of the traffic during the winter season. 

The data can be found at https://data.dtu.dk/collections/AIS_Trajectories_from_Danish_Waters_for_Abnormal_Behavior_Detection/6287841

To cite this work:
Olesen, Kristoffer Vinther; Christensen, Anders Nymark; Clemmensen, Line Katrine Harder (2023). AIS Trajectories from Danish Waters for Abnormal Behavior Detection. Technical University of Denmark. Collection. https://doi.org/10.11583/DTU.c.6287841.v1
