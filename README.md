# Blue Button 2.0 Analytics (bbanalytics)

Author: mark
Created: 2019-06-19.07:51

# bbanalytics

This repository has a sample of more than 3,000
ExplanationOfBenefit Bundles from the CMS Blue Button 2.0 API.

The fanalyze.py script runs through the EOB bundles 
and creates summary files. These can be useful to
identify synthetic beneficiaries with various conditions,
or with different types of claims. 

## Create virtual environment

    python -m venv venv

Activate Virtualenv

    source ./venv/bin/activate

    
## Create summary files

    chmod +x ./fanalyze.py
    ./fanalyze.py
    
After the code completes you can find two results
files in ./data

- eob_results.csv
- eob_summary.json



    
    
    
