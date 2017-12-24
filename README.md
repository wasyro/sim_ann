# sim_ann
Solve TSP(Japanese Prefectures) using simulated annealing  

# Environment
Python 3.6.2  
Anaconda3 - 5.0.0  
drawnow - 0.71.3  

# How To
'lonlat_to_xy.py' converts longtitude and latitude to x-y coordinates.  
input file needs to be shaped;  
(longtitude0) (latitude0)  
(longtitude1) (latitude1)  
(longtitude2) (latitude2)  
.  
.  
.  
lontitude0 and latitude0 are coordinates of the original point in an x-y plane.  

If you play the demo, please execute;  
    $ pip install drawnow

# References
Kirkpatrick, et al, 1983, Optimization by Simulated Annealing, *Science*, Vol.220, No. 4598. pp. 671-680.  
David Bookstaber, 1997, Simulated Annealing for Traveling Salesman Problem, http://www.bookstaber.com/david/opinion/SATSP.pdf
