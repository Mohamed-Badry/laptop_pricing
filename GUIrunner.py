import sys

from utils import load_model, load_transformers
from predictorGUI import evaluate, PredictWinodw, Predict # importing our model, view, controller respectively
from PyQt5.QtWidgets import QApplication

def main():
    """
    Run the laptop price predictor model with the GUI to provide input
    """
    
    model_path = 'models/rmse318.pkl'
    model = load_model(model_path)

    les = load_transformers()

    data_format = {
        'Status': None,
        'Brand': None,
        'Model': None,
        'CPU': None,
        'RAM': None,
        'Storage': None,
        'Storage type': None,
        'GPU': None,
        'Screen': None,
        'Touch': None,
    }

    notes = {
        'Status': None,
        'Brand': None,
        'Model': None,
        'CPU': None,
        'RAM': "GB",
        'Storage': "GB",
        'Storage type': None,
        'GPU': None,
        'Screen': "in",
        'Touch': None,
    }

    for key in data_format:
        if key in les:
            data_format[key] = les[key].classes_

    app = QApplication([])
    with open("style.css") as f:
        app.setStyleSheet(f.read())
        
    window = PredictWinodw(mlModel=model, format=data_format, notes=notes)
    window.show()
    predictor = Predict(model=evaluate, view=window, transformers=les)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
