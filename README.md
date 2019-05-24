Automated Cryptocurrency Algorithmic Trading
============================================

Poynor & Bradshaw, LLC.

#### STRUCTURE
```
--> README.MD
--> TA
	|--> algo1.py
	|--> algo2.py
--> ML
	|--> algo3.py
	|--> algo4.py
--> backend
	|--> apicontroller.py
	|--> logs
		|--> log1.csv
		|--> log2.csv
--> master.py
--> deps
	|--> localdep1.py
	|--> localdep2.py
--> data
	|--> scraper.py
	|--> apis
		|--> source1api.py
		|--> source2api.py
	|--> hodl
		|--> dataset1.csv
		|--> trainingdata.xml
		|--> dataset2.csv
--> testbed? TBD...
```

#### TRADING ROUTINE
```
| master python script in home directory |

 | | |
 v v v 

| algorithm script from one of the algo subdirs |

 | | |
 v v v 

| API controller file (backend subdir) | 

 | | |
 v v v

| POST request to exchange API |

 | | |
 v v v

| response logged via controller file |

 | | |
 v v v

| recorded in logs dir |
```

#### DATA COLLECTION ROUTINE

```
| scraper.py in data subdir|

 | | |
 v v v

| python scraper in apis folder |

 | | |
 v v v

| data in the hodl directory |

 | | |
 v v v 

| ML algorithms (hopefully we can run them in background on server to train) | 
```

TESTING ROUTINE
===============

	tbd.... depends on backend API / exchange we choose

