# 558 Perfume

## Development Instructions

### 0. setting a virtual environment, preparing to connect

* check existing virtualenv using

    ```shell
    conda env list
    ```

* activate virtualenv by

    ```shell
    conda activate env_name
    ```

* deactivate it

    ```shell
    conda deactivate
    ```

### 1. connecting to neo4j database

* download  Neo4j Desktop at <https://neo4j.com/download-center/#cyphershell>;

* open Neo4j Desktop, click on "Graph Apps" in the left column, then open "Neo4j Browser";

* in Neo4j Browser, click on  ":server connect", and input the folowing info:

  - Connect URL: <neo4j+s://36d638c4.databases.neo4j.io>
  - Authentication type: Username / Password
  - Username: neo4j
  - Password: 1McmE-lDtVUMYBPUFsiQKscrqbD4M58Oc1hJOcKulcM

### 2. importing data into database

* run example.py by command line under ./neo4j/ with:

    ```shell
    python example.py
    ```

### 3. front-end framework -- Django

* paradise-papers-django is an example django-neo4j framework

## Overview

### Motivation

This project aims to build a Knowledge Graph towards Perfume Industry.

For detailed project motivation, challenges and datasource, please refer to our proposal or [click here](/proposal.md).

### Structure

Project's tree-structured directories present as follows:

```text
.
├── 558 propopal 0.pdf
├── 558 propopal 1.pdf
├── PRsystem
│   ├── LICENSE
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── Procfile
│   ├── README.md
│   ├── credentials-e1ccd058.env
│   ├── docs
│   ├── newest_requirements.txt
│   ├── paradise_papers_search
│   └── requirements.txt
├── Perfume Comparison and Recommendation System.pdf
├── README.md
├── crawler
│   ├── Amazon
│   ├── FragranceNet_Crawler
│   ├── Sephora
│   └── modules
├── data
│   ├── amazon.jsonl
│   ├── final_perfume_data.csv
│   ├── fragranceNet.jsonl
│   ├── fragrancenet.json
│   ├── fragrancenet1.json
│   └── sephora.jsonl
├── idea.txt
├── neo4j
│   └── example.py
├── ontology.png
├── proposal.md
├── tmp
└── tree
```

## Data

To be implemented.
