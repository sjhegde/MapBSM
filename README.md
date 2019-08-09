# MapBSM
MapBSM is a tool which allows for Connected Vehicle movements to be visualized on a Leaflet map in real-time.

# Motivation
This tool exists for Connected Vehicle deployers or testers to visualize vehicles moving through their deployment corridor. This project was created by the Saxton Transportation Operations Laboratory, funded by the Federal Highway Administration.

# Example at the Turner-Fairbank Highway Research Center
![Settings Window](https://github.com/sjhegde/MapBSM/blob/master/MapBSMimage.PNG)

# Framework
MapBSM works with a Python processing script `BSMVisBackend.py` that reads new lines in a Connected Vehicle Basic Safety Message csv log and updates the location of the vehicle associated with each ID in the file or drops the vehicle associated with an ID if that ID is no longer being used (IDs are temporary according to SAE J2735). `BSMVisBackend.py` then caches the list of active vehicles which is then served on a local Flask development server. The mapping html file then uses `leaflet-realtime` and pulls data from the local Flask server. 

# Installation

MapBSM requires Python3, Flask, Pandas, and Numpy, as well as the Python `datetime`, `cs`, `time`, and `json` packages. 

```
pip install Python3
pip install Flask 
pip install pandas
pop install numpy
```


# Use

Edit `BSMVisBackend.py` to navigate to your BSM log file. By default, the Python processing file looks for a csv log file called `realtimeBSMs.csv`. 

To run the Python init method and launch the Flask server run (on Windows): 

```
>>> mapping.bat
```
