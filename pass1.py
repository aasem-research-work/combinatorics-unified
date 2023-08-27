from math import factorial
from itertools import combinations
import pandas as pd


def gen_combination(nn, rr):
    numbers = range(1, nn + 1)
    return list(combinations(numbers, rr))


def combin(number, number_chosen):
    return factorial(number) // (factorial(number_chosen) * factorial(number - number_chosen))


def dic_to_pd(dic, columns):
    df = pd.DataFrame.from_dict(dic, orient='index')
    df.index.name = 'Row'
    df.columns = [f'Column {i + 1}' for i in range(columns)]
    return df


def pass1(n, r):
    pass1_stats = {}
    combinations_result = combin(n, r)
    columns = n * (n - 1) // r
    rows = combinations_result // columns
    num_of_rep_per_row = n - 1
    total_rep_per_row = ((n - 1) * combinations_result) // (n * (n - 1) // r)

    if combinations_result % columns == 0:
        pass1_stats["combinations"] = combinations_result
        pass1_stats["columns"] = columns
        pass1_stats["rows"] = rows
        pass1_stats["row-wise repetitions"] = num_of_rep_per_row
        pass1_stats["Total repetitions"] = total_rep_per_row

        result = gen_combination(n, r)
        #print("Length of result:", len(result))

        result_dic = {}
        for row in range(rows):
            col = result[row * columns: (row + 1) * columns]
            result_dic[row + 1] = col
        output_df = dic_to_pd(result_dic, columns)
        valid_bool = True
    else:
        print("Invalid parameters")
        output_df = None
        valid_bool = False

    return valid_bool, pass1_stats, output_df


if __name__ == '__main__':
    # Ask for N and R
    n = int(input("N: "))
    r = int(input("R: "))
    valid_bool, pass1_stats, output_df = pass1(n, r)

    if valid_bool:
        print("\ncombinations:", pass1_stats["combinations"])
        print("columns:", pass1_stats["columns"])
        print("rows:", pass1_stats["rows"])
        print("Numbers repetitions in each row:",
              pass1_stats["row-wise repetitions"])
        print("Total numbers occurs in combinations",
              pass1_stats["Total repetitions"])

        # Save the DataFrame to an Excel file
        # output_file_path = f'output_N{n}_R{r}.xlsx'
        output_file_path = 'output.xlsx'
        print(f"The result has been saved to {output_file_path}")
        output_df.to_excel(output_file_path, engine='openpyxl')
