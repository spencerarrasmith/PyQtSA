widgetStyle_mainWindow = \
    """
    .QFrame {
        background: white;
        }
    
    QToolTip {
        background-color: white;
        color: black;}
    """

widgetStyle_splash = \
    """
    QSplashScreen {font: 14pt Segoe UI;}
    """

widgetStyle_popup = \
    """
    QDialog {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #FFFFFF, stop: 0.4 #E5E5E5,
                                   stop: 0.5 #DDDDDD, stop: 1.0 #D8D8D8);
        font: 14pt Segoe UI; 
        }
    
    QLabel {
        font: 14pt Segoe UI; 
        }
    
    QLineEdit {
        background: white;
        font: 14pt Segoe UI; 
        }
    
    QPushButton {
        background: #D2D2D2;
        font: 14pt Segoe UI; 
        }
    
    QSpinBox {
        background: white;
        font: 14pt Segoe UI; 
        }
    
    QDoubleSpinBox {
        background: white;
        font: 14pt Segoe UI; 
        }
    """

widgetStyle_tabBar = \
    """
    QTabWidget::pane { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                   stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);}
    
    QTabBar::tab:!selected {font: 12pt Segoe UI;
                            color: #888888;
                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #DDDDDD, stop: 0.6 #D2D2D2,
                                stop: 0.7 #C8C8C8, stop: 1.0 #999999);
                            /*border-top-right-radius: 4px;
                            border-top-left-radius: 4px;*/
                            border-bottom-color: #CCCCCC;
                            margin-top: 2px;
                            margin-left: 1px;
                            margin-right: 1px;}
    
    QTabBar::tab:selected {font: 18pt Segoe UI;
                          color: black;
                          background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #F6F6F6, stop: 0.7 #E8E8E8,
                                            stop: 0.8 #E5E5E5, stop: 1.0 #E1E1E1);
                          border-bottom-color: #E0E0E0;
                          margin-top: 3px;
                          margin-left: 1px;
                          margin-right: 1px;
                          }
    """

widgetStyle_QSATab = \
    """
    QFrame {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                   stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
        }
    
    QFrame>QGroupBox {
        border: 1px solid #CCCCCC;
        background-color: white;
        }
    """

widgetStyle_QSAParameterCluster = \
    """
    QGroupBox {
        font: 14pt Segoe UI;
        border: 1px solid #CCCCCC;
        background-color: white;
        }
    QGroupBox>QLabel {
        font: 14pt Segoe UI;
        border: 0px;
        }
    QLabel {
        font: 14pt Segoe UI;
        background-color: white;
        color: #000000;
        border: 0px;
        }
    
    .QLabel {font: 14pt Segoe UI;}
    .QDoubleSpinBox {font: 14pt Segoe UI;}
    .QPushButton {font: 14pt Segoe UI;}
    """

widgetStyle_QSABaseFrame = \
    """
    QFrame {
        border: 1px solid #CCCCCC;
        background-color: white;
        }
    QFrame>QLabel {
        border: 0px;
        }
    """

widgetStyle_constantsExpand = \
    """
    .QPushButton {
        background-color: #B92526;
        color: white;
        border-radius: 12px;
        }
    """

widgetStyle_spinboxSet = \
    """
    QDoubleSpinBox {
        selection-background-color: #B92526;
        color: black;
        }
    """

# background-color: #EEEEEE;

# background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
# stop: 0  # EEEEEE, stop: 0.9 #EEEEEE,
# stop: 0.95  # B92526, stop: 1.0 #B92526);


widgetStyle_textActual = \
    """
    QLabel {
        background-color: white;
        color: #771111;
        border: 0px;
        }
    """

widgetStyle_spinboxActual = \
    """
    QDoubleSpinBox {
        background-color: white;
        color: #771111;
        border-radius: 3px;
        }
    """

widgetStyle_tabActive = \
    """
    QGroupBox {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #F6F6F6, stop: 0.7 #E8E8E8,
            stop: 0.8 #E5E5E5, stop: 1.0 #E1E1E1);
        color: #FFFFFF;
        border-radius: 0px;
        }
    
    QLabel {
        font: 18pt Segoe UI;
        }
    """

widgetStyle_tabInactive = \
    """
    QGroupBox {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #DDDDDD, stop: 0.6 #D2D2D2,
            stop: 0.7 #C8C8C8, stop: 1.0 #999999);
        color: #771111;
        border-radius: 3px;
        }
    """

widgetStyle_constantsCluster = \
    """
    QDialog {
        background-color: #CCCCCC
        }
    """

widgetStyle_blankSpace = \
    """
    QFrame {
        background-color: #FFFFFF
        }
    """

widgetStyle_QSAPushbutton = \
    """
    QPushButton {
        background-color: #EEEEEE
        }
    """

widgetStyle_toggleButtonEnable = \
    """
    QPushButton {
        background-color: #CCFFCC
        }
    """

widgetStyle_toggleButtonDisable = \
    """
    QPushButton {
        background-color: #FFCCCC
        }
    """

widgetStyle_infoFrameGood = \
    """
    QFrame {
        border: 1px solid #A0A0A0;
        background-color: #CCFFCC;
        }
    QFrame>QLabel {
        border: 0px;
        background-color: #CCFFCC;
        }
    """

widgetStyle_infoFrameBad = \
    """
    QFrame {
        border: 1px solid #A0A0A0;
        background-color: #FFCCCC;
        }
    QFrame>QLabel {
        border: 0px;
        background-color: #FFCCCC;
        }
    """

widgetStyle_mathFrameGood = \
    """
    QFrame {
        border: 1px solid #A0A0A0;
        background-color: #CCFFCC;
        font: 12pt Segoe UI;
        }
    QFrame>QLabel {
        border: 0px;
        background-color: #CCFFCC;
        font: 12pt Segoe UI;
        }
    """

widgetStyle_mathFrameBad = \
    """
    QFrame {
        border: 1px solid #A0A0A0;
        background-color: #FFCCCC;
        font: 12pt Segoe UI;
        }
    QFrame>QLabel {
        border: 0px;
        background-color: #FFCCCC;
        font: 12pt Segoe UI;
        }
    """