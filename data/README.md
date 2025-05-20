# Data

This directory contains all raw and processed data to populate the database. 

This directory uses the following tree structure

```
.
├── README.md
└── {datasource}/
    └── README.md
    └── raw/
    └── processed/
```

where `README.md` describes the datasource and the `raw/` directory store the unprocessed data while `processed/` stores the data ready to be imported into the database

The processed data is processed using a python script in `scripts/processing/{datasource}`


