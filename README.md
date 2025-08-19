
# Salesforce Glue Backup 

## DIRS
│
├── README.md
├── provider.tf       # puts the state files in `state_files\`
├── s3.tf             # creates the data bucket; creates script bucket; uploads scripts 
├── glue.tf           # create the Glue job to run `sf_get.py`
├── iam.tf            # role for Glue/S3
├── variables.tf      # 
├── terraform.tfvars  # define the bucket, script and Glue job names
├── output.tf         # output for infos
├── scripts/
│   ├── sf_get.py     # script to use the SalesForce API to get chunked data
│   └── queries.json  # queries `sf_get.py` will run to retrieve data
├── test/   # test the inital connection to Salesforce vi Docker
│   ├── Dockerfile
│   ├── test.py
│   └── buildme.sh
├── state_files/
│   ├── terraform.tfstate
│   └── terraform.tfstate.backup
└── .gitignore

The Glue Py script pulls SalesForce API credentials from SecretsManager.
(The Secret is created manually put into `tfvars`.)

That script will read in queries from `queries.json` and push them to the S3 bucket (tfvars).
The `queries.json` will contain 1..n queries defining the dataset to pull.

This package is designed to run inside an Amazon Linux 2023 image with Admin role rights attached.
