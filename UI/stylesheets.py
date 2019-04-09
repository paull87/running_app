calendar_popup = """QToolButton {\n
height: 20px;\n
width: 70px;\n
color: white;\n
font-size: 14px;\n
icon-size: 20px, 20px;\n
background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333);\n
}\n
QMenu {\n
width: 150px;\n
left: 20px;\n
color: white;\n
font-size: 14px;\n
background-color: rgb(100, 100, 100);\n
}\n
QSpinBox { \n
width: 70px; \n
font-size:14px; \n
color: white;  \n
background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333);\n
selection-background-color: transparent;\n
selection-color: rgb(255, 255, 255);\n
}\n
QSpinBox::up-button { subcontrol-origin: border; subcontrol-position: top right; width:20px; }\n
QSpinBox::down-button {subcontrol-origin: border; subcontrol-position: bottom right; width:20px;}\n
QSpinBox::up-arrow { width:10px; height:20px; }\n
QSpinBox::down-arrow { width:10px; height:20px; }\n
QWidget { alternate-background-color: rgb(128, 128, 128); }\n
QAbstractItemView:enabled \n
{\n
font-size:10px; \n
color: rgb(180, 180, 180); \n
background-color: black; \n
selection-background-color: rgb(64, 64, 64); \n
selection-color: rgb(0, 255, 0); \n
}\n
QWidget#qt_calendar_navigationbar\n
{ \n
background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333); \n
}\n
\n
QAbstractItemView:disabled \n
{ \n
color: rgb(64, 64, 64); \n
}"""

calendar_summary = """
QLabel {
  font-size: 16px;
  font-family:'Helvetica', sans-serif;
}"""