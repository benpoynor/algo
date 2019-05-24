STRUCTURE:
==========
```
- README.MD<br/>
- TA<br/>
	* algo1.py<br/>
	* algo2.py<br/>
- ML<br/>
	* algo3.py<br/>
	* algo4.py<br/>
- backend<br/>
	- apicontroller.py<br/>
	- logs<br/>
		- log1.csv<br/>
		- log2.csv<br/>
- master.py<br/>
- deps<br/>
	- localdep1.py<br/>
	- localdep2.py<br/>
- data<br/>
	- scraper.py<br/>
	- apis<br/>
		- source1api.py<br/>
 		- source2api.py<br/>
	- hodl<br/>
		- dataset1.csv<br/>
		- trainingdata.xml<br/> 
		- dataset2.csv<br/>
- testbed? TBD...<br/>
```

TRADING ROUTINE
===============
| master python script in home directory |

 | | |<br/>
 v v v 

| algorithm script from one of the algo subdirs |

 | | |<br/>
 v v v 

| API controller file (backend subdir) | 

 | | |<br/>
 v v v

| POST request to exchange API |

 | | |<br/>
 v v v

| response logged via controller file |

 | | |<br/>
 v v v

| recorded in logs dir |


DATA COLLECTION ROUTINE
=======================

| scraper.py in data subdir|

 | | |<br/>
 v v v

| python scraper in apis folder |

 | | |<br/>
 v v v

| data in the hodl directory |

 | | |<br/>
 v v v 

| ML algorithms (hopefully we can run them in background on server to train) | 


TESTING ROUTINE
===============

	tbd.... depends on backend API / exchange we choose

