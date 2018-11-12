# import csv
# import operator
from argparse import ArgumentParser
from top_counts import TopCounts
from utils import sort_values, add_percentage

# class TopCounts(object):
#     """
#     Computes top counts for a read in CSV file 
    
#     Args:
#         input_filename (str): CSV file
#         occupation_output_filename (str): filename where to save occupation output 
#         state_output_filename (str): filename where to save state output 
#         delimiter (str): CSV delimiter character 
#         quotechar (str): Quote character in CSV file 

#     Attributes:
#         input_filename (str): CSV filename
#         occupation_output_filename (str): occupation output filename
#         state_output_filename (str): state output filename
#         delimiter (str): delimiter character for read and write  
#         quotechar (str): Quote character
#     """
#     def __init__(self, input_filename, occupation_output_filename, state_output_filename, 
#                  delimiter=';', quotechar='"'):
#         self.input_filename = input_filename
#         self.occupation_output_filename = occupation_output_filename
#         self.state_output_filename = state_output_filename
#         self.delimiter = delimiter
#         self.quotechar = quotechar
             
#     def compute_counts(self, certified_value='CERTIFIED', status='STATUS', 
#                              soc_col='SOC_NAME', state_col='EMPLOYER_STATE'):
#         """
#         Computes counts for desired column field based on column names 
#         Args:
#             certified_value (str): status to subset data -- default (CERTIFIED)
#             status (str): Status column name -- default (STATUS)
#             soc_col (str): Standard Occupational Classification column name -- default (SOC_NAME)
#             state_col (str): State column name -- default (EMPLOYER_STATE)
#         Returns:
#             counts (dict): dictionary of {desired_col : count}
#             N (int): total number of certified applications regardless of occupation
#         """
#         # initialize dicts 
#         occupation_counts = {}
#         state_counts = {}
#         with open(self.input_filename, 'r') as f:
#             # read file 
#             lines = csv.reader(f, quotechar=self.quotechar, delimiter=self.delimiter,
#                              quoting=csv.QUOTE_ALL)
#             # get column names
#             columns = next(lines)
#             # get indicies 
#             status_index, occ_index, state_index = self._get_indices(columns, status=status, 
#                                                                     soc_col=soc_col, state_col=state_col)
#             # get total number of certified applications regardless of occupation
#             N = 0
#             for line in lines:
#                 # only if status == CERTIFIED
#                 if line[status_index].lower() == certified_value.lower():
#                     occ = line[occ_index]
#                     state = line[state_index]
#                     N += 1
#                     # increment count based on occupation
#                     if occ not in occupation_counts:
#                         occupation_counts[occ] = 0
#                     occupation_counts[occ] += 1
#                     # increment count based on state
#                     if state not in state_counts:
#                         state_counts[state] = 0
#                     state_counts[state] += 1
                    
#         # return count dicts and total number of certified applications regardless of occupation
#         return occupation_counts, state_counts, N

#     def _split_col_name(self, col_name):
#         """
#         returns list of lowered split column name
#         """
#         return [col.lower() for col in col_name.split('_')]


#     def _get_indices(self, header_columns, status, soc_col, state_col):
#         """
#         return indices value of status, occupation and state columns
#         """
#         try:
#             # get split soc_col and state_col 
#             soc_col_names = self._split_col_name(soc_col)
#             state_col_names = self._split_col_name(state_col)
#             # loop through all column names 
#             for i, split_col in enumerate([col.split('_') for col in header_columns]):
#                 for split in split_col:
#                     # lower 
#                     split = split.lower()
#                     if status.lower() in split:
#                         status_index = i
#                     # handles both `SOC_NAME` and `LCA_CASE_SOC_NAME` and custom 
#                     if soc_col_names[-2] and soc_col_names[-1] in split:
#                         occ_index = i
#                     # # handles both `EMPLOYER_STATE` and `LCA_CASE_EMPLOYER_STATE`
#                     if state_col_names[-2] and state_col_names[-1] in split:
#                         state_index = i
#             return status_index, occ_index, state_index
#         # handle exception
#         except UnboundLocalError:
#             raise Exception('COLUMN NAMES NOT FOUND. PLEASE CHECK COLUMN NAMES')
#         except IndexError:
#             raise Exception('COLUMN NAMES NOT FOUND. PLEASE CHECK COLUMN NAMES')

#     def write_to_file(self, top, filename, col2='NUMBER_CERTIFIED_APPLICATIONS', col3='PERCENTAGE'):
#         """
#         Saves output to output_filename
#         Args:
#             top (list): top N list of tuples [(desired_col, counts), ...]
#             filename (str): filepath where to save output 
#             col2 (str): Name of counts column 
#             col3 (str): Name of percentage column
#         """
#         # get column nam from passed in output file name 
#         name = filename.split('_')[-1].split('.')[0].upper()
#         with open(filename, 'w') as f:
#             # write column names
#             f.write('TOP_{}'.format(name) + self.delimiter + \
#                     col2  + self.delimiter + col3 + '\n')
#             # write data 
#             for line in top:
#                 line = self.delimiter.join(map(str, line))
#                 f.write(line + '\n')
        

def main():
    parser = ArgumentParser()
    parser.add_argument('input_filename', help='read CSV file from input_filename', type=str, metavar='FILE 1')
    parser.add_argument('occupation_output_filename', help='write report to occupation_output_filename', 
                        type=str, metavar='FILE 2')
    parser.add_argument('state_output_filename', help='write report to state_output_filename', 
                        type=str, metavar='FILE 3')
    parser.add_argument('-topN', '--topN', help='number of top occurances -- default(10)', type=int, default=10)
    parser.add_argument('-c', '--status_level', help='STATUS LEVEL -- default(CERTIFIED)', type=str, default='CERTIFIED')
    parser.add_argument('-a', '--status_col', help='STATUS COLUMN NAME -- default(STATUS)', type=str, default='STATUS')
    parser.add_argument('-o', '--occupation_col', help='OCCUPATION COLUMN NAME -- default(SOC_NAME)', type=str, default='SOC_NAME')
    parser.add_argument('-s', '--state_col', help='STATE COLUMN NAME -- default(EMPLOYER_STATE)', type=str, default='EMPLOYER_STATE')
    args = parser.parse_args()
    print(args)
    # initialize model 
    top_model = TopCounts(input_filename=args.input_filename, 
                               occupation_output_filename=args.occupation_output_filename,
                               state_output_filename=args.state_output_filename, 
                               delimiter=';')
    # compute counts 
    occ_counts, state_counts, N = top_model.compute_counts(certified_value=args.status_level, 
                                status=args.status_col, soc_col=args.occupation_col, state_col=args.state_col)
    # sort occupation and state and by top N
    top_occs = sort_values(occ_counts, top_N=args.topN)
    top_states = sort_values(state_counts, top_N=args.topN)
    # Add percentage of applications that have been certified
    top_occs = add_percentage(top_occs, N)
    top_states = add_percentage(top_states, N)
    # write to file 
    top_model.write_to_file(top_occs, top_model.occupation_output_filename)
    top_model.write_to_file(top_states, top_model.state_output_filename)

if __name__ == '__main__':
    main()
    

