from utils import transform_data

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QComboBox, QLabel, QGridLayout,
    QWidget, QLineEdit, QPushButton, QCompleter
)


class _ClearableLineEdit(QLineEdit):
    """ helper class for custom line edit boxes"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def mousePressEvent(self, event):
        self.clear()
        super().mousePressEvent(event)
    

class _SLineEdit(QLineEdit):
    """ helper class for the line edit boxes in combo boxes """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setReadOnly(True)
        
    def mousePressEvent(self, event):
        pass
    
    def mouseReleaseEvent(self, event):
        self.parent().showPopup()


class _SelectableComboBox(QComboBox):
    """ custom combo box """
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addItems(choices)
        self.setEditable(False)  # Enable typeahead
        self.setLineEdit(_SLineEdit())  # Set the custom QLineEdit
        
        # Create and configure the QCompleter
        completer = QCompleter()
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setModel(self.model())
        self.setCompleter(completer)
        
    def mousePressEvent(self, event):
        pass
    
    def mouseReleaseEvent(self, event):
        self.showPopup()


class PredictWinodw(QMainWindow):
    """ 
    The GUI for the predictor (view) 
    
    parameters:
    
        mlModel: 
            The machine learning model that will do the prediction
            
        format: dict
            A dictionary that has the format of the data, its keys are
            the labels and its values are either 'None' for numerical
            data that the user inputs or a list of possible values to make a combobox
            key -> label
            value -> list of options or None
            
        notes (optional): dict
            A dictionary representing notes that can go next to the labels,
            key -> label
            value -> note string
    """

    def __init__(self, mlModel, format, notes=None):
        super().__init__()
        self.setWindowTitle('Predictor')
        self.mlModel = mlModel
        self.format = format
        self.notes = notes

        self.layout = QGridLayout()

        self._createButton()
        self._createInputBoxes()
        self._createDisplay()

        widget = QWidget(self)
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def _createButton(self):
        self.button = QPushButton('Predict')
        self.layout.addWidget(self.button, len(self.format), 0)

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display, len(self.format), 1)

    def _createInputBoxes(self):
        def combo_box(options):
            """ helper function to create a combo box """
            cbox = _SelectableComboBox(options)
            return cbox

        def editable_box():
            """ helper function to create an editable text box """
            text_in = _ClearableLineEdit()
            text_in.setPlaceholderText("Enter a number...")
            return text_in

        self.data_widgets = {}
        for key, choices in self.format.items():
            
            # handles notes 
            try:
                note = self.notes[key]
            except (TypeError, KeyError):
                note = None

            if note is None:
                _label = QLabel(f"{key}: ")
            else:
                _label = QLabel(f"{key} ({note}): ")
                
            # handles creating the proper widget depending on the format values provided
            if choices is not None:
                self.data_widgets[key] = (_label, combo_box(choices))
            else:
                self.data_widgets[key] = (_label, editable_box())

        for i, (key, widgets) in enumerate(self.data_widgets.items()):
            self.layout.addWidget(widgets[0], i, 0)
            self.layout.addWidget(widgets[1], i, 1)

    def getData(self):
        self.data = {}
        try:
            for key in self.data_widgets:
                if self.format[key] is None:
                    self.data[key] = [float(self.data_widgets[key][1].text())]
                else:
                    text = str(self.data_widgets[key][1].currentText())
                    self.data[key] = [text]
        except ValueError as e:
            self.setDisplayText("Error: invalid input data")
            # print(e)
        return self.data

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def getModel(self):
        return self.mlModel


class Predict():
    """ 
    The controller class for the predictor. 
    
    parameters:
        model: function
            the function that handles the logic of the app
            
        view: QMainWindow
            the class that handles the GUI
            
        transformers: dict
            the transformers used on the data loaded into a dictionary
            key -> label
            value -> labelEncoder()
    """

    def __init__(self, model, view, transformers):
        self._evaluate = model
        self._view = view
        self._les = transformers
        self._connectSignalAndSlots()

    def _predictTarget(self):
        self._view.setDisplayText("Processing...")
        data = self._view.getData()
        try:
            result = str(self._evaluate(
                mlModel=self._view.getModel(), data=data, transformers=self._les))
        except (KeyError, ValueError) as e:
            # print("Exception occurred:", e) # Debugging statement
            result = "Error: invalid input data"
        self._view.setDisplayText(result)

    def _connectSignalAndSlots(self):
        self._view.button.clicked.connect(self._predictTarget)
        self._view.display.returnPressed.connect(self._predictTarget)


def evaluate(mlModel, data, transformers):
    """ Predict the target (Model) """
    data_t = transform_data(data, transformers)
    return round(mlModel.predict(data_t)[0], 2)
