import UI.FilesControllerUI as fcui


class WidgetBuilder(fcui):
    def __init__(self):
        super()

        




    def initLabels(self, label = fcui.QLabel, text = "", color = None, fontFam = "", fontSi = 0, fontBold = bool,):
            """ Label setup """
            label.setText(text)
            if type(color) is str:
                label.setStyleSheet(f"color: {color};")
            else:
                label.setStyleSheet(f"color: rgb({color[0]}, {color[1]}, {color[2]});")
            font = fcui.QFont()
            font.setFamily(f"{fontFam}")
            font.setPointSize(fontSi)
            font.setBold(fontBold)
            label.setFont(font)
            label.setAlignment(fcui.Qt.AlignCenter)

    def validatorLineEdit(self, lineEdit = fcui.QLineEdit, QRegExpText = ""):
        #"[0-9]+.?[0-9]{,2}"
        reg_ex = fcui.QRegularExpression(QRegExpText)
        input_validator = fcui.QRegularExpressionValidator(reg_ex, lineEdit)
        lineEdit.setValidator(input_validator)