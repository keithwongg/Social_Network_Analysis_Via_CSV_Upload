# Social Network Analysis Via CSV Upload

## Introduction

A *[SMU BIA] (https://www.smubia.org/) X *[Orca Active] (https://orcaactive.com/) collaboration. Orca Active sells female athleisure clothing, and this project aims to aid them in identifying customers of great influence via Social Network Analytics. The influence of a customer can be split into Quantitative and Qualitative portions. Quantitative assessment involves numerical representations via metrics such as degree of centrality, eigenvector centrality and betweenness centrality. Qualitative assessment includes things such as personality, style, genuine communication with others without the intention to oversell, i.e. trustworthiness and likeability. 

In this project, the focus will be mainly on the Quantitative portion with the use of a CSV upload by exporting out data from Orca Active's shopify storefront. Metrics Used: Degree of Centrality (# of connections for a node), Eigenvector Centrality (a more meaningful way to calculate centrality), Betweenness Centrality (to identify nodes that are strong connectors).


## Getting Started
The following instructions will get the project up and running on your local machine for development and testing purposes.

## Prerequisites
Ensure that the following are installed via pip:
* [Django 3.0.6.] (https://www.djangoproject.com/download/) - The current Django version used in this project
* [Python 3.7.6] (https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/) - Recommended to use this version to prevent any unexpected errors.
* [NetworkX] (https://networkx.github.io/documentation/stable/install.html) - Used to calculate centrality. 

### Running this project
Open terminal (make sure that the path is where you store the files -- Alternatively, if you use VSCode, just go to Terminal > New Terminal and a new terminal with the current path will be opened at the bottom of the screen.)

Run:
```
python3 manage.py runserver
```
If everything goes well, terminal will show: 
```
Django version 3.0.7, using settings 'networkanalysis.settings'
Starting development server at <Local Host>
Quit the server with CONTROL-C.
```
Copy and paste the link (local host) provided into a browser and the application would be up and running.

## Tech Stack/ Frameworks
Front-End:
- Bootstrap
- JQuery
- AnyChart
- HTML, CSS, JS
- Django Templates

Back-End:
- Django (Python)
- NetworkX (Python - To process and calculate Centrality Metrics)


## Authors
Keith Wong Jun Hsien (Singapore Management University)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgements

