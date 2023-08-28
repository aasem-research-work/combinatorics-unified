import pandas as pd
import numpy as np
from ast import literal_eval
from collections import defaultdict


def count_frequency(df, n):
    # Initialize lists and dictionaries for storing frequency counts and statistics
    frequency_list = []
    mean_list = []
    std_list = []

    # Iterate through each row in the input DataFrame df
    for index, row in df.iterrows():
        # Initialize frequency dictionary with keys ranging from 1 to n and values initialized to 0
        frequency_dict = defaultdict(int, {i: 0 for i in range(1, n + 1)})

        # Iterate through each cell in the row
        for cell in row:
            if isinstance(cell, str):
                # Evaluate the string into a list of numbers
                numbers = literal_eval(cell)

                # Update frequency dictionary based on these numbers
                for number in numbers:
                    frequency_dict[number] += 1

        # Calculate the mean and standard deviation of the numbers in the row
        total_numbers = sum(frequency_dict.values())
        mean = total_numbers / n
        std = np.sqrt(
            sum((frequency_dict[i] - mean) ** 2 for i in range(1, n + 1)) / n)

        # Append the results to lists
        frequency_list.append(frequency_dict)
        mean_list.append(mean)
        std_list.append(std)

    # Create Output DataFrames based on these lists
    returned_df = pd.DataFrame(frequency_list)
    stats_df = pd.DataFrame({'mean': mean_list, 'std': std_list})

    return returned_df, stats_df


def swap(df, col_A_index, row_A, col_B_index, row_B):
    # Get the column names by their indices
    col_A = df.columns[col_A_index]
    col_B = df.columns[col_B_index]

    # Temporarily store the value at (col_A, row_A)
    temp = df.at[row_A, col_A]

    # Swap the value at (col_A, row_A) with the value at (col_B, row_B)
    df.at[row_A, col_A] = df.at[row_B, col_B]

    # Swap the value at (col_B, row_B) with the temporarily stored value
    df.at[row_B, col_B] = temp

def swap_dic2df(df, col_A_index, row_A, col_B_index, row_B):
    # Get the column names by their indices
    col_A = df.columns[col_A_index]
    col_B = df.columns[col_B_index]

    # Retrieve the row index
    row_A_index = df.index[row_A]
    row_B_index = df.index[row_B]

    # Temporarily store the value at (col_A, row_A_index)
    temp = df.at[row_A_index, col_A]

    # Swap the value at (col_A, row_A_index) with the value at (col_B, row_B_index)
    df.at[row_A_index, col_A] = df.at[row_B_index, col_B]

    # Swap the value at (col_B, row_B_index) with the temporarily stored value
    df.at[row_B_index, col_B] = temp


def count_frequency_dic2df(df, n):
    frequency_list = []
    mean_list = []
    std_list = []

    for _, row in df.iterrows():
        # Initialize frequency dictionary
        frequency_dict = defaultdict(int, {i: 0 for i in range(1, n + 1)})

        for cell in row:
            if isinstance(cell, (list, tuple)):
                for number in cell:
                    frequency_dict[number] += 1

        # Calculate the mean and standard deviation
        total_numbers = sum(frequency_dict.values())
        mean = total_numbers / n
        std = np.sqrt(
            sum((frequency_dict[i] - mean) ** 2 for i in range(1, n + 1)) / n)

        # Append to lists
        frequency_list.append(frequency_dict)
        mean_list.append(mean)
        std_list.append(std)

    # Convert to DataFrames
    returned_df = pd.DataFrame(frequency_list)
    stats_df = pd.DataFrame({'mean': mean_list, 'std': std_list})

    return returned_df, stats_df

def bruteforce_dic2df(df):
    row_count, col_count = df.shape

    # Start the row and column index from 0
    row = 0
    col = 0

    # Outer loop
    while row < row_count:
        # Get cell value at [row, col]
        cellA = df.iloc[row, col]
        row_A = row
        col_A_index = col

        # Inner loop
        for next_row in range(row + 1, row_count):
            # Get cell value at [next_row, col]
            cellB = df.iloc[next_row, col]
            row_B = next_row
            col_B_index = col

            # Perform swap
            swap_dic2df(df, col_A_index=row_A, row_A=col_A_index,
                        col_B_index=row_B, row_B=col_B_index)

        # Move to the next column and reset row to 0 for the next iteration
        col += 1
        row = 0

        # If reached the last column, break the loop
        if col >= col_count:
            break


if __name__ == "__main__":
    # Load output.xlsx and extract "Sheet1" as df
    df = pd.read_excel("output.xlsx", sheet_name="Sheet1", engine='openpyxl')

    # Call count_frequency function
    #returned_df, stats_df = count_frequency(df, n=4)

    print(df.head())

    # swap(df, col_A_index, row_A, col_B_index, row_B)
    swap(df, col_A_index=1, row_A=0, col_B_index=1, row_B=1)

    print(df.head())
    #print("Returned DF:", returned_df)
    #print("Stats DF:", stats_df)
