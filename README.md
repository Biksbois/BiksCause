# BiksCause

This Git contains the code from the paper *'Inferring causal relationships from temporal events'*.
Authors: Roni Horo, Mads H. Kusk, Jeppe J. Holt and Bjarke S. Baltzersen, all currently studying Computer Science at Aalborg University.

When executiong this program, certain dependecies are required, and can be found in the `requirements.txt` file, but can also be seen here. They are as follows:

```
jenkspy==0.2.0
tqdm==4.60.0
pandas==1.2.3
numpy==1.19.5
```

When executing the program, run the `main.py` file. This file does however need you to specify a few things. This is first of all what dataset you wish to execute on, and as of now there are three supported datasets. These include:

* __Synthetic__: The synthetic dataset will run on 100 syntheticly generated datasets.
* __Traffic__: This is an Experiments on the Metro Interstate Traffic Volume Dataset ([here](https://archive.ics.uci.edu/ml/datasets/Metro+Interstate+Traffic+Volume)) and find causality between traffic volume and weather events.
* __Air__: This experiment is based on the Beijing Multi-Site Air-Quality Data Data Set ([here](https://archive.ics.uci.edu/ml/datasets/Beijing+Multi-Site+Air-Quality+Data)). This dataset contains information about weather and pollution levels in Beijing from several spots in the city. The dataset utilized in this case is the test site Dongsi.

In addition to the dataset, you should also specify what you wish to run. This can be:

* __Generate__: The effect of this keyword will depend on the context. If you run on the synthetic dataset, __generate__ will generate 100 new datasets and if it is __air__ the dataset will be split into seasons. In the case of __traffic__ nothing will happen.
* __Cluster__: This will generate clusters on the dataset. The effect will be the same no matter what the specified dataset is.
* __Experiment__: This will run the experiment. For the synthetic dataset, this will run the experiment one time for each dataset (100 times), for air one time per season and for traffic just one time. This will find causal pairs based on eight different scores, including three different CIR scores and the NST where each score has a variant with and without clusters, adding up to a combined eight scores.
* __Result__: This will show all the results from the experiment.
* __Window__: This will find an idea lag value. If this is not selected, the default window sizes will be [1, 5, 10, 18, 24]
* __All__: This will run everything.

When running the program, one dataset should be specified and one to many commands. Exampels could be:

```
python main.py synthetic experiment
```

if you wish to run experiments on the synthetic dataset, or

```
python main.py air experiment result
```

if you wish to run the experiments and show the results for the air dataset.

In terms of the hyper parameters when running the experiments, they will as a default be as following:

* window_size = 1, 5, 10, 6, 12, 18, 24
* alpha_val = 0.55, 0.66, 0.77
* lambda_val = 0.4, 0.5, 0.7    
* k_vals = 10, 15, 20, 25
* support = 10
* dataset_count = 100

where the __windows_size__ represents how far each of the scores look back when searching for causality. The __alpha_val__ and __lambda_val__ is specific for the NST score. The __k_vals__ represents how the Hits@K analysis will be conducted when running the __result__ command and the support decides the limit for how many times an event must occur in the dataset before we will deem it relevant. At last, the __dataset_count__ represents how many datasets are generated when the `synthetic generate` command is executed.


