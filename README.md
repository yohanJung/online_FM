# Online Factorization Machine

## Getting Started

This project compares the recent reseach of the online Factoriztiaon machine for regression and classficatino task. We figure out the pros and cons for recent research. We will propose the revised model to overcome the limitation of online factorization machince.

## Dataset

### regression task <br/>

movielens 100k - https://grouplens.org/datasets/movielens/ <br/>
cod-rna - https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/ <br/>
YearPredictionMSD - https://archive.ics.uci.edu/ml/datasets/yearpredictionmsd/ <br/>
### classfication task <br/>
cod-rna - https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/ <br/>
Frappe - https://github.com/hexiangnan/neural_factorization_machine/tree/master/data/frappe/ <br/>
    

## Model

1. FM + FTRL <br/>
/models/FM_FTRL.py
2. SFTRL <br/>
/models/SFTRL_CCFM.py (refactored code by pytorch)  <br/>
/models/SFTRL_Vanila.py (refactored code by pytorch)  <br/> 
3. OCCFM - working
4. RRF <br/>
/models/RRF.py <br/>
/models/RRF_Online.py (refactored code by pytorch)  <br/> 
    
## Run experiment

run_bash.sh or run_bach_all.sh (test_argparse.py)
   
    
## Reference paper

1. Factorization Machines -S Rendle et al.
2. Sketched Follow-The-Regularized-Leader for Online Factorization Machine -Luo Luo et al.
3. Online Compact Convexified Factorization Machine -Wenpeng Zhang et al.
4. Ad Click Prediction: a View from the Trenches -H. Brendan McMahan et al.
5. Large-scale Online Kernel Learning with Random Feature Reparameterization -Tu Dinh Nguyen et al. <br/>
6. Scalable Variational Bayesian Factorization Machine -Avijit Saha et al.

## Reference code

https://github.com/bmdy/SFTRL <br/>
https://github.com/tund/RRF <br/>
https://github.com/rishabhmisra/Scalable-Variational-Bayesian-Factorization-Machine <br/>
https://github.com/cemoody/vfm <br/>

## Funding

This research was supported by the Korean MSIT (Ministry of Science and ICT), under the National Program for Excellence in SW (2016-0-00018), supervised by the IITP (Institute for Information & communications Technology Planning&Evaluation)

## Contributor

yohan Jung 
