# Cardiac Comparator
App to provide a UI to compare synthetic/real cardiac echos to evaluate a generative AI!

Author: @akashc1


### Setup
Clone this repository:
```
git clone git@github.com:akashc1/cardiac_comparator.git
```

Create a new conda environment & install the required libraries:
```
cd cardiac_comparator
conda create --prefix <PATH_PREFIX> -n 'compare' --file requirements.txt python=3.10
```

### Run on Sherlock
(On Sherlock) Start streamlit server:
```
streamlit run comparator.py
```

(On local machine) Start ssh tunnel:
```
ssh -L <PORT>:<REMOTE_HOST>:<PORT> <SUID>@login.sherlock.stanford.edu
```

Example if the streamlit server is running on `sh03-11n01`:
```
ssh -L 8501:sh03-11n01:8501 login.sherlock.stanford.edu
```

Navigate to page in browser: http://localhost:8501

### Run locally
Start streamlit server:
```
streamlit run comparator.py
```

Navigate to page in browser: http://localhost:8501
