
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog

from ui_main import Ui_MainWindow
from pass1 import pass1
from pass2 import count_frequency_dic2df, swap_dic2df,bruteforce_dic2df
import pandas as pd
from ast import literal_eval


class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        self.pass2_df = None

        # Connect signals to custom slots
        self.actionImport.triggered.connect(self.apply_import)
        self.actionExport.triggered.connect(self.apply_export)
        self.pushButton_genCombinations.clicked.connect(self.apply_pass1)
        self.pushButton_swap.clicked.connect(self.apply_swap)
        self.pushButton_Rearrange.clicked.connect( self.get_selected_items_from_table)
        #self.pushButton_Rearrange.clicked.connect( self.apply_bruteforce)
        
    def apply_bruteforce(self):
        #bruteforce_dic2df(self.pass2_df)
        pass

    def get_info_from_imported(self, df):
        unique_values = set()
        R = 0

        for index, row in df.iterrows():
            for cell in row:
                if isinstance(cell, str):
                    # Convert the string representation of a tuple into an actual tuple
                    tuple_values = literal_eval(cell)

                    # Update R based on the length of the tuple
                    R = max(R, len(tuple_values))

                    # Add unique values to the set
                    unique_values.update(tuple_values)

        # Calculate N based on the total number of unique values
        N = len(unique_values)

        return N, R

    def apply_export(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if fileName:
            if not fileName.endswith('.xlsx'):
                fileName += '.xlsx'
            print(f"Saving file to: {fileName}")

            try:
                self.pass2_df.to_excel(
                    fileName, sheet_name='Sheet1', engine='openpyxl', index=True)
                print(f"Successfully saved to {fileName}")
            except Exception as e:
                print(f"An error occurred while saving: {e}")

    def apply_import(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if fileName:
            print(f"Chosen file: {fileName}")
            # Load the Excel file into a DataFrame
            try:
                imported_df = pd.read_excel(
                    fileName, sheet_name='Sheet1', engine='openpyxl')
                # Convert the DataFrame to have an index-based structure
                # Assuming 'Row' is the index column in the Excel sheet
                imported_df.set_index('Row', inplace=True)
                # Now, imported_df should be in the desired format
                self.N_value = 9
                self.R_value = 4

                # Populate tableWidget_passes with output_df
                self.returned_df, self.stats_df = count_frequency_dic2df(
                    imported_df, self.N_value)
                self.populate_table_widget(self.tableWidget_pass1, imported_df)
                self.populate_table_widget(self.tableWidget_pass2, imported_df)
                self.pass2_df = imported_df

                # Populate tableWidget_pass2_freq with returned_df
                self.populate_table_widget(
                    self.tableWidget_pass2_freq, self.returned_df)

                N, R = self.get_info_from_imported(self.pass2_df)

                self.spinBox_N.setValue(N)
                self.spinBox_R.setValue(R)
                self.N_value = N
                self.R_value = R

                if self.N_value >= 0 and self.R_value >= 0 and self.R_value <= self.N_value:
                    #self.valid_bool, pass1_stats, output_df = calc_stats(imported_df)
                    self.valid_bool = False
                else:
                    self.valid_bool = False

                self.update_stats()

            except Exception as e:
                print(f"An error occurred: {e}")

    def get_selected_items_from_table(self):
        selected_dict = {}
        selected_items = self.tableWidget_pass2.selectedItems()
        for item in selected_items:
            row = item.row()
            col = item.column()
            value = item.text()

            # Create a (row, col) tuple key for the dictionary
            key = (row, col)

            # Store the value in the dictionary
            selected_dict[key] = value

        return selected_dict

    def populate_table_widget(self, table_widget, df):
        table_widget.setRowCount(df.shape[0])
        table_widget.setColumnCount(df.shape[1])
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                table_widget.setItem(i, j, item)

    def apply_pass1(self):
        self.N_value = self.spinBox_N.value()
        self.R_value = self.spinBox_R.value()

        if self.N_value >= 0 and self.R_value >= 0 and self.R_value <= self.N_value:
            self.valid_bool, pass1_stats, output_df = pass1(
                self.N_value, self.R_value)
        else:
            self.valid_bool = False

        if self.valid_bool:
            # Update textBrowser_pass1stats
            stats_text = "\n".join(
                [f"{key}: {value}" for key, value in pass1_stats.items()])
            self.textBrowser_pass1stats.setPlainText(stats_text)

            # Populate tableWidget_passes with output_df
            self.returned_df, self.stats_df = count_frequency_dic2df(
                output_df, self.N_value)
            self.populate_table_widget(self.tableWidget_pass1, output_df)
            self.populate_table_widget(self.tableWidget_pass2, output_df)
            self.pass2_df = output_df

            # Populate tableWidget_pass2_freq with returned_df
            self.populate_table_widget(
                self.tableWidget_pass2_freq, self.returned_df)

            self.update_stats()
        else:
            self.textBrowser_pass1stats.setPlainText("Invalid parameters")

    def apply_swap(self):
        selected_dict = self.get_selected_items_from_table()
        i = 0
        for k, v in selected_dict:
            if i == 0:
                col_A_index_value = v
                row_A_value = k
            elif i == 1:
                col_B_index_value = v
                row_B_value = k
            i += 1

        if i > 1:
            swap_dic2df(self.pass2_df, col_A_index_value,
                        row_A_value, col_B_index_value, row_B_value)
            self.populate_table_widget(self.tableWidget_pass2, self.pass2_df)
            self.update_stats()

    def update_stats(self):
        # Populate tableWidget_pass2_freq with returned_df
        self.returned_df, self.stats_df = count_frequency_dic2df(
            self.pass2_df, self.N_value)
        self.populate_table_widget(
            self.tableWidget_pass2_freq, self.returned_df)
        # Populate tableWidget_pass2_stats with stats_df
        self.populate_table_widget(self.tableWidget_pass2_stats, self.stats_df)
        self.tableWidget_pass1.resizeColumnsToContents()
        self.tableWidget_pass2.resizeColumnsToContents()
        self.tableWidget_pass2_freq.resizeColumnsToContents()
        self.tableWidget_pass2_stats.setHorizontalHeaderLabels([
            "AVG", "STD"])
        self.tableWidget_pass2_stats.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()
