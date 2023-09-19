# IUCN-Data-Scraping
Repository created to aid a research project of Maastricht Science Project to create a brochure highlighting 
wildlife and their levels of endangerment based on the IUCN

## Information
The IUCN data Scraping aimed to retrieve select information from a set of IUCN links to a specific animal in order to 
extract the following information: _Scientific name_, _criteria_, _Country_, _justification_, _assessors_.

**Note:** There does exist an IUCN API requiring registration which unfortunately takes some time to go through. Please 
use the API and plan ahead with time to spare for the registration process before running the 
this data scraping process. The API will provide a far more efficient and easier approach to accessing data. This 
scraping process should be used as a second resort. 

## Project Structure
The project is arranged as follows:
```
errors/
    # Contains IUCN links where scraping errors occured
links/
    # Contains the original list of IUCN links for scraping
results/
    # Contains the scraped information for each set of links
main.py  # Execution of the data scraping process
envrionment.yml  # Conda virtual environment
position.csv  # Simple position update when scraping
```

## Environment
The `environment.yml` file contains all required dependencies for the project. 
In order to construct the Conda virtual environment, please run the following steps:
### 1. Create the Environment
```
conda env create -f environment.yml
```

### 2. Activate the Environment
```
conda activate IUCN-data
```

### 3. Specify Environment in your IDE
If you are using VScode or PyCharm, please select the created environment as the environment to use.
Here is the link for how to accomplish this on PyCharm: https://www.jetbrains.com/help/pycharm/conda-support-creating-conda-virtual-environment.html

## How to Use
### 1. Create a csv file containing IUCN links
Place this file inside the `links/` directory.
Example links are as follows (please also review the links directory for further examples):
```
https://dx.doi.org/10.2305/IUCN.UK.2022-1.RLTS.T179055548A179055550.en
https://dx.doi.org/10.2305/IUCN.UK.2022-1.RLTS.T179056157A179056160.en
https://dx.doi.org/10.2305/IUCN.UK.2022-1.RLTS.T179086396A179086399.en
```
Please specify the links file name on line 27 in the `main.py` file as in the below example:
```
links_file = "links/no_justification_links.csv"
```

### 2. Set Position to Zero
Within the position.csv file, please set the number to 0. This allows a new position to be held for the file to read in. 
For each new file you read please reset this to zero. 
If you need to stop and restart the program at any point, the position ensures you do not have to repeat any previous scrapes.


### 3. Specify the Results File 
Please specify the name of your results csv file on line 28 as in the example below:
```
results_file = "results/data_no_justification.txt"
```

If no file is yet found, the code will create the file. If the file already exists, new information will be appended to it. 

#### 4. Specify the Errors File
The errors file contains the links at which data scraping was not successful. The links are saved for potential manual scraping.
Please specify the name of the errors csv file on line ... as in the below example:
```
errors_file = "errors/errors_no_justification.txt"
```
If no file is yet found, the code will create the file. If the file already exists, new information will be appended to it.