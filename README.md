# Social Network Analysis Via CSV Upload

## Introduction

A [SMU BIA](https://www.smubia.org/) X Orca Active project. Orca Active, a female athleisure brand (due for launch end 2020), worked together with SMU BIA, to come up with a project to help them identify customers of major influence via Social Network Analytics (SNA). The influence of a customer can be split into Quantitative and Qualitative portions. Quantitative assessment involves numerical representations via metrics such as degree of centrality, eigenvector centrality and betweenness centrality. Qualitative assessment includes things such as personality, style, genuine communication with others without the intention to oversell, i.e. trustworthiness and likeability. 

In this project, the focus will be mainly on the Quantitative portion with the use of a CSV upload by exporting out data from Orca Active's shopify storefront. Metrics Used: Degree of Centrality (number of connections for a node), Eigenvector Centrality (importance of a node and not just the number of connections), Betweenness Centrality (to identify nodes that are strong connectors).


## Getting Started
The following instructions will get the project up and running on your local machine for development and testing purposes.

## Prerequisites
Ensure that the following are installed via pip:
* [Django 3.0.6.](https://www.djangoproject.com/download/) - The current Django version used in this project
* [Python 3.7.6](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/) - Recommended to use this version to prevent any unexpected errors.
* [NetworkX](https://networkx.github.io/documentation/stable/install.html) - Used to calculate centrality. 

### Running this project
**Open the project files:** Open terminal (make sure that the path is where you store the files -- Alternatively, if you use VSCode, just go to Terminal > New Terminal and a new terminal with the current path will be opened at the bottom of the screen.)

**Make the following changes in settings.py:**
1. Replace the 'SECRET_KEY' variable in settings.py with your own secret key (in Python String format), generated from either by [Django's get_random_secret_key() module](https://humberto.io/blog/tldr-generate-django-secret-key/), or [this website](https://djecrety.ir/). A secret key is generated every time a new django project is created and the project cannot run without it.
2. Change DEBUG variable from **False** to **True**.

**Run:**
```
python3 manage.py runserver
```

If everything goes well, terminal will show: 
```
Django version 3.0.7, using settings 'networkanalysis.settings'
Starting development server at <Local Host>
Quit the server with CONTROL-C.
```
Copy and paste the link (i.e. local host address) provided into a browser and the application would be up and running.

Alternatively, you can try out this project [here](https://socialnetworkanalytics.herokuapp.com/); hosted on Heroku.

## Tech Stack/ Frameworks
Front-End:
- [Bootstrap](https://getbootstrap.com/) - CDN
- [JQuery](https://jquery.com/) - CDN
- [AnyChart](https://www.anychart.com/) - CDN
- [Django Templates](https://docs.djangoproject.com/en/3.0/topics/templates/)
- HTML, CSS, JavaScript

Back-End:
- [Django 3.0.6.](https://www.djangoproject.com/download/) (Python)
- [NetworkX](https://networkx.github.io/documentation/stable/install.html) (Python - To process and calculate Centrality Metrics)


## Authors
Keith Wong Jun Hsien (Singapore Management University)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
