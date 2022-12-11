from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Ui_MainWindow():
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.txt_nodes = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_nodes.setGeometry(QtCore.QRect(90, 50, 121, 31))
        self.txt_nodes.setObjectName("txt_nodes")
        self.lbl_nodes = QtWidgets.QLabel(self.centralwidget)
        self.lbl_nodes.setGeometry(QtCore.QRect(20, 60, 47, 13))
        self.lbl_nodes.setObjectName("lbl_nodes")
        self.lbl_branches = QtWidgets.QLabel(self.centralwidget)
        self.lbl_branches.setGeometry(QtCore.QRect(20, 110, 47, 13))
        self.lbl_branches.setObjectName("lbl_branches")
        self.txt_branches = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_branches.setGeometry(QtCore.QRect(90, 100, 121, 31))
        self.txt_branches.setObjectName("txt_branches")
        self.lbl_rows = QtWidgets.QLabel(self.centralwidget)
        self.lbl_rows.setGeometry(QtCore.QRect(20, 160, 47, 13))
        self.lbl_rows.setObjectName("lbl_rows")
        self.txt_rows = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_rows.setGeometry(QtCore.QRect(90, 160, 121, 61))
        self.txt_rows.setObjectName("txt_rows")
        self.btn_graph = QtWidgets.QPushButton(self.centralwidget)
        self.btn_graph.setGeometry(QtCore.QRect(50, 240, 75, 23))
        self.btn_graph.setObjectName("btn_graph")         
        self.lbl_tie = QtWidgets.QLabel(self.centralwidget)
        self.lbl_tie.setGeometry(QtCore.QRect(120, 330, 47, 13))
        self.lbl_tie.setObjectName("lbl_tie")
        self.lbl_cut = QtWidgets.QLabel(self.centralwidget)
        self.lbl_cut.setGeometry(QtCore.QRect(380, 330, 47, 13))
        self.lbl_cut.setObjectName("lbl_cut")
        self.matrix_tie = QtWidgets.QTextBrowser(self.centralwidget)
        self.matrix_tie.setGeometry(QtCore.QRect(20, 360, 256, 192))
        self.matrix_tie.setObjectName("matrix_tie")
        self.matrix_tie.setFontPointSize(16.0)
        self.matrix_cut = QtWidgets.QTextBrowser(self.centralwidget)
        self.matrix_cut.setGeometry(QtCore.QRect(290, 360, 256, 192))
        self.matrix_cut.setObjectName("matrix_cut")
        self.matrix_cut.setFontPointSize(16.0)
        self.btn_calculate = QtWidgets.QPushButton(self.centralwidget)
        self.btn_calculate.setGeometry(QtCore.QRect(160, 240, 75, 23))
        self.btn_calculate.setObjectName("btn_calculate")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.btn_graph.clicked.connect(lambda: self.drawGraph(self.add_rows(self.txt_rows.toPlainText())))
        self.btn_calculate.clicked.connect(lambda: self.calculate_sets(self.add_rows(self.txt_rows.toPlainText())))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CAD Solver"))
        self.lbl_nodes.setText(_translate("MainWindow", "Nodes:"))
        self.lbl_branches.setText(_translate("MainWindow", "Branches:"))
        self.lbl_rows.setText(_translate("MainWindow", "Matrix:"))
        self.btn_graph.setText(_translate("MainWindow", "Graph"))
        self.lbl_tie.setText(_translate("MainWindow", "Tie-Set:"))
        self.lbl_cut.setText(_translate("MainWindow", "Cut-Set:"))
        self.btn_calculate.setText(_translate("MainWindow", "Calculate"))


    def add_rows(self,rows):
        nodes=int(self.txt_nodes.toPlainText())
        branches=int(self.txt_branches.toPlainText())
        incidence_matrix=np.zeros_like(a=None, shape=(nodes,branches))
        rows_matrix=str(rows).split('/')
        for i in range(len(rows_matrix)):
            current_row=rows_matrix[i].split(',')
            for j in range(branches):
                incidence_matrix[i][j]= current_row[j]
        
        # print(incidence_matrix)
        return incidence_matrix
        
        
    def calculate_sets(self, incidence_matrix):
        A= np.array(incidence_matrix)
        A= A[:-1,:]
        tree_branches= int(self.txt_nodes.toPlainText())-1
        #full_branches= int(self.txt_branches.toPlainText())
        #links=full_branches-tree_branches+1
        A_tree= A[:tree_branches, :tree_branches]
        #A_link= A[:tree_branches, tree_branches:]
        A_tree=np.float64(A_tree)
        A=np.float64(A)
        
        A_tree_inv= np.linalg.inv(A_tree)
        for i in range(len(A_tree_inv)):
            for j in range(len(A_tree_inv)):
                if(A_tree_inv[i][j]== -0):
                    A_tree_inv[i][j]= 0
        cut_set= np.dot(A_tree_inv, A)
        # print(A_tree_inv)
        # print(A)
        # print(cut_set)
        C_link= cut_set[:tree_branches, tree_branches:]
        B_tree= (C_link * -1).T
        B_tree_rows, B_tree_cols= B_tree.shape
        for i in range(B_tree_rows):
            for j in range(B_tree_cols):
                if(B_tree[i][j]== -0):
                    B_tree[i][j]= 0
        
        self.matrix_cut.setText(str(cut_set))
        self.matrix_tie.setText(str(B_tree))




    def drawGraph(self, incidence_matrix):
        incidence_matrix= np.int64(np.array(incidence_matrix))
        print(incidence_matrix)
        edges= []
        #This loop cycles nodes(incidence_matrix rows)
        for node in range(0, len(incidence_matrix[:])):
            current_row=list(incidence_matrix[node])
            current_node_connections= list()

        #This loop cycles the values in the current row
            for i in range(0, len(current_row)):
                #base_node= current_row[i]
                if(current_row[i] !=1):
                    continue
        #This loop cycles the values in the current column
                for j in range(0, (len(incidence_matrix[:]+1))):
                    #end_node= incidence_matrix[j][i]
                    #Compare the values in the current column to the base node
                    #If the next column value is zero then there's no connection
                    if (incidence_matrix[j][i] !=0 ):
                        if(current_row[i] > incidence_matrix[j][i]):
                            #If base node > value in the column below then a connection comes from this node to the node with the negative number
                            current_node_connections.append(j+1)
            
            edges.append(current_node_connections)

        #We have 2 lists, one for nodes and one for edges, we want to combine them into a dictionary where key=node and value=list of connections
        dict= {}
        nodes_list=[i for i in range(1,len(edges)+1)]

        for i in range(0,len(nodes_list)):
            dict[(nodes_list[i])] = (edges[i])

        print(dict)

        #Draw the graph
        
        graph=nx.DiGraph(dict)
        pos= nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_size=400)
        nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), edge_color='black')
        nx.draw_networkx_labels(graph,pos)
        
        plt.show()
    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
