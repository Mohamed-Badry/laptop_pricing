# Laptop Price Predictor (w/GUI for input)


## Description
A ML model that uses sklearn's `GradientBoostingRegressor` to train on the laptop price data available on this [kaggle page](https://www.kaggle.com/datasets/juanmerinobermejo/laptops-price-dataset) then used along with a GUI made with PyQt5 so that a user can provide laptop features and get a price prediction on button click.


## Repo Contents

### Folders:
- `data`: Where data is stored. 
- `models`: Where models are stored. 
- `transformers`: Where transformers are stored.
- `images`: Where images are stored.

### Files:
- `requirements.txt`: The required libraries to run the files in this repo.
- `laptop_pricing.ipynb`: The analysis of the data, model training, and evaluation is done here. 
- `utils.py`: Utility functions to load the model, and the transformers, and transform the data. 
- `predictorGUI.py`: GUI API (built around the MVC design paradigm) made to provide easy user input through comboboxes and display the result on button click.  
- `style.css`: CSS style sheet for the `predictorGUI.py`.  
- `GUIrunner.py`: This file runs the GUI app with the laptop price predicting model to ask the user.


## How to use the project locally
Start by cloning the repo to your device and make a new environment.

### Install the required dependencies

    pip install -r requirements.txt

### Run the model with the GUI

    python3 GUIrunner.py

Now a window like the following shows up where you can input the laptop features to get a price prediction.


<p align="center">
    <img src="images\image_2024-02-05_225839551.png" alt="Alt image text" />
</p>


## Notes

I made the `predictorGUI.py` to be reusable with other projects where precise string input would be required as having the input provided by comboboxes eliminates the mistakes that a user provides in the data strings, though further testing is required.