

import requests
import pandas as pd
import os


charts2 = pd.read_csv('../charts2.csv')

os.system('cls||clear')


def query_request(query):
    api_url = 'http://localhost:8000/search/?query=' + query
    return requests.get(api_url)
    
def chart_query_request(query, Id):
    api_url = 'http://localhost:8000/search/charts/'+ Id +'/?query='+query
    return requests.get(api_url)

finished = False

print('**********************************************************************************')
print('*                                                                                *')
print('*                                    WELCOME!!                                   *')


print('\nEnter quit as patient name to quit.\n')

while not finished:

        initial_list=[]
        final_list =[]
        query = ''

        disp_frame = charts2

        first_pass=True
        
        while (len(final_list) != 1) and (query !='quit'):
            
            if first_pass == False:
                if (len(final_list) == 0):
                    print('\nNo patient meets your criteria.\n')
                else:    
                    print('\nYour query is not.\nThe following patients match the initial query.')
                    print('Please narrow down your search to one patient from the list below:\n')
                    initial_list = final_list

            final_list =[]     

            print(disp_frame[{'Id', 'Name', 'Gender'}].head(10))

            query = input('\nID or Name of Patient: ')

            response = query_request(query)
            for hit in response.json()['hits']:
                final_list.append(hit['_source'])
            if (len(final_list)>0):
                disp_frame = pd.DataFrame(final_list)
            first_pass = False


        final_frame = pd.DataFrame(final_list)
        
        
        if query != 'quit':

            selection = 0

            print('\nYou have selected the cart for:\n')
            print(final_frame[{'Id', 'Name'}])
            Id = final_frame.iloc[0, 0]
            
            while (selection != '99'):
                print('\nPatient ' + Id + '\'s chart consists of:\n')
                field_numbers = len(final_frame.columns)
                for field, column in zip(range(field_numbers), final_frame.columns):
                    print(field, column)
                selection = input ('\nEnter a number to display the chart element, type a search term to search chart, or 99 to select another chart: ')
                if selection != '99':
                    if selection.isnumeric() and int(selection) in range (0, field_numbers):
                        print('\nThe result of your query:')
                        for line in final_frame.iloc[:,int(selection)]:
                            print(line)
                    else:
                        query = selection
                        response = chart_query_request(query, Id)
                        chart_hit = response.json()['hits']
                        print('\nThe result of your query:\n')
                        if len(chart_hit) > 0 :
                            highlights=chart_hit[0]['highlight']
                            results = []
                            for individuals in highlights.items():
                                results.append(individuals)
                            for result in results:
                                print(result)
                        else:
                            print('No Matching Information')

            
           
                  
        finished = (query == 'quit')
        
