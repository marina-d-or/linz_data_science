import csv

import pandas as pd

# hardcoded to allow large data cells
csv.field_size_limit(9262144)

# index of where property owner names are in the LINZ CSV file
NAME_INDEX = 9


def read_linz_csv(file_path='C:/Users/alexg/Downloads/nz-property-titles-including-owners.csv'):

    linz_data = pd.read_csv(file_path)

    # column_names_list = linz_data.columns.tolist()
    #
    # # Print the list of column names
    # print(column_names_list)
    # result_df = linz_data[linz_data['id'] == 4476977]
    # result_df=result_df['owners'].str.split(',')
    # #res=result_df.loc[0, 'owners']
    # print('len = ',result_df)
    linz_data=linz_data.dropna(subset=['owners'])
    number_of_properties=linz_data.shape[0]
    #print('number of properties with owners = ', linz_data.shape[0])

    linz_data['owners'] = linz_data['owners'].str.split(',')
    #print(type(linz_data['owners'][0]))
    linz_data_exploded = linz_data.explode('owners')
    linz_data_exploded=linz_data_exploded.reset_index(drop=True)
    #print('linz_data_exploded', linz_data_exploded.shape)

    # Group by 'owners' and count occurrences
    owner_counts = linz_data_exploded['owners'].value_counts()
    #print('number of different names = ', owner_counts.shape, type(owner_counts))

    investors = owner_counts[owner_counts > 1]
    investors = investors.reset_index(drop=False)
    invest_property=linz_data_exploded[linz_data_exploded['owners'].isin(investors['owners'])]
    number_of_investment_properties = invest_property['id'].nunique() #number of investment properties
    # invest_property_counts=invest_property['id'].value_counts()
    # number_of_investment_properties = invest_property_counts.shape[0]
    #print('number_of_investment_properties = ', number_of_investment_properties)
    number_of_non_investment_properties=number_of_properties-number_of_investment_properties
    #print('number_of_non_investment_properties = ', number_of_non_investment_properties)

    # Filter to keep only rows where 'id' appears more than once
    # owner_counts = owner_counts[owner_counts > 1]
    # print('q', owner_counts.shape)
    result_df = pd.DataFrame({'id': owner_counts.index, 'quantity': owner_counts.values})
    #print('more than one id', result_df.loc[250:300])
    result={'number of properties': number_of_properties, 'number of investment properties': number_of_investment_properties, 'number of non-investment properties':number_of_non_investment_properties}
    return result



# def find_records_without_empty_owner_names(linz_data):
#     new_linz_data = []
#     for item in linz_data:
#         if item[NAME_INDEX] == '':
#             new_linz_data.append(item.copy())
#     return new_linz_data


def assess_investement_properties(linz_data):
    print('second function')
    number_of_properties = len(linz_data)
    number_of_investment_properties = 0
    col = len(linz_data[0])  # initial number of columns
    print('number of columns = ', col, ', number of rows = ', number_of_properties)
    i = 0
    dict_of_names = {}   #dict_of_names[name] = [i, k]: i - index in linz_data, k - number of properties that name has
    list_of_indices = []
    # print (type(linz_data[i][ind]))
    while i < number_of_properties:
        investment = False
        for name in linz_data[i][NAME_INDEX]:

            if name in dict_of_names:
                investment = True  # binary_search(dict_of_names, name)>-1:          # name in dict_of_names:
                # a =dict_of_names.index(name)
                # ('name = ', name, 'i=', i, 'a = ',a, 'b=', dict_of_names[a-1:a])
                if len(linz_data[i]) == col:
                    linz_data[i].append(1)
                else:
                    linz_data[i][-1] = 1
                k = dict_of_names[name][0]  # list_of_indices[dict_of_names.index(name)][1]
                linz_data[k][-1] = 1
                # if name=='':
                #     print(linz_data[i])
                dict_of_names[name][1] += 1

            else:
                # print('no name = ', name)
                if len(linz_data[i]) == col:
                    linz_data[i].append(0)
                dict_of_names[name] = [i, 1]  # insert_into_sorted_list(dict_of_names, name)
                # list_of_indices.append([name,i])
        if investment:
            number_of_investment_properties += 1
        i += 1
    # j=0
    # for name in tuple_of_names:
    #     print(j, 'empty name? ',name)
    #     j+=1
    return [linz_data, number_of_investment_properties, dict_of_names]

file_path = 'C:/Users/alexg/Downloads/nz-property-titles-including-owners.csv'
linz_data = read_linz_csv(file_path)
if __name__ == "__main__":
    file_path = 'C:/Users/alexg/Downloads/nz-property-titles-including-owners.csv'
    linz2_data = read_linz_csv(file_path)

    #data = find_records_without_empty_owner_names(linz_data)

    #print(linz_data.loc[0])