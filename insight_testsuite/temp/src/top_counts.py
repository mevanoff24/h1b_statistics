import csv

class TopCounts(object):
    """
    Computes top counts for a read in CSV file 
    
    Args:
        input_filename (str): CSV file
        occupation_output_filename (str): filename where to save occupation output 
        state_output_filename (str): filename where to save state output 
        delimiter (str): CSV delimiter character 
        quotechar (str): Quote character in CSV file 

    Attributes:
        input_filename (str): CSV filename
        occupation_output_filename (str): occupation output filename
        state_output_filename (str): state output filename
        delimiter (str): delimiter character for read and write  
        quotechar (str): Quote character
    """
    def __init__(self, input_filename, occupation_output_filename, state_output_filename, 
                 delimiter=';', quotechar='"'):
        self.input_filename = input_filename
        self.occupation_output_filename = occupation_output_filename
        self.state_output_filename = state_output_filename
        self.delimiter = delimiter
        self.quotechar = quotechar
             
    def compute_counts(self, certified_value='CERTIFIED', status='STATUS', 
                             soc_col='SOC_NAME', state_col='WORKSITE_STATE'):
        """
        Computes counts for desired column field based on column names 
        Args:
            certified_value (str): status to subset data -- default (CERTIFIED)
            status (str): Status column name -- default (STATUS)
            soc_col (str): Standard Occupational Classification column name -- default (SOC_NAME)
            state_col (str): State column name -- default (EMPLOYER_STATE)
        Returns:
            counts (dict): dictionary of {desired_col : count}
            N (int): total number of certified applications regardless of occupation
        """
        # initialize dicts 
        occupation_counts = {}
        state_counts = {}
        with open(self.input_filename, 'r') as f:
            # read file 
            lines = csv.reader(f, quotechar=self.quotechar, delimiter=self.delimiter,
                             quoting=csv.QUOTE_ALL)
            # get column names
            columns = next(lines)
            # need atleast three columns
            assert len(columns) >= 3
            # get indicies 
            status_index, occ_index, state_index = self._get_indices(columns, status=status, 
                                                                    soc_col=soc_col, state_col=state_col)
            # print(columns[31])
            print(status_index, occ_index, state_index)
            # get total number of certified applications regardless of occupation
            N = 0
            for line in lines:
                # print(line)
                # only if status == CERTIFIED
                if line[status_index].lower() == certified_value.lower():
                    occ = line[occ_index]
                    state = line[state_index]
                    N += 1
                    # remove missing values 
                    if occ:
                        # increment count based on occupation
                        if occ not in occupation_counts:
                            occupation_counts[occ] = 0
                        occupation_counts[occ] += 1
                    # remove missing values 
                    if state:
                        # increment count based on state
                        if state not in state_counts:
                            state_counts[state] = 0
                        state_counts[state] += 1
                    
        # return count dicts and total number of certified applications regardless of occupation
        return occupation_counts, state_counts, N

    def _split_col_name(self, col_name):
        """
        returns list of lowered split column name
        """
        return [col.lower() for col in col_name.split('_')]


    # def _get_indices(self, header_columns, status, soc_col, state_col):
    #     """
    #     return indices value of status, occupation and state columns
    #     """
    #     try:
    #         # get split soc_col and state_col 
    #         soc_col_names = self._split_col_name(soc_col)
    #         # print('HERE', soc_col_names[-2], soc_col_names[-1])
    #         state_col_names = self._split_col_name(state_col)
    #         # loop through all column names 
    #         for i, split_col in enumerate([col.split('_') for col in header_columns]):
    #             # print(split_col)
    #             for split in split_col:
    #                 # lower 
    #                 split = split.lower()
    #                 if status.lower() in split:
    #                     status_index = i
    #                 # handles both `SOC_NAME` and `LCA_CASE_SOC_NAME` and custom 
    #                 if soc_col_names[-2] and soc_col_names[-1] in split:
    #                     occ_index = i
    #                 # # handles both `EMPLOYER_STATE` and `LCA_CASE_EMPLOYER_STATE`
    #                 if state_col_names[-2] and state_col_names[-1] in split:
    #                     print(split_col, state_col)
    #                     state_index = i
    #         return status_index, occ_index, state_index
    #     # handle exception
    #     except UnboundLocalError:
    #         raise Exception('COLUMN NAMES NOT FOUND. PLEASE CHECK COLUMN NAMES')
    #     except IndexError:
    #         raise Exception('COLUMN NAMES NOT FOUND. PLEASE CHECK COLUMN NAMES')

    # def check_if_included(self, split_col, desired_col):
        # """Check if all values are included in split column"""
        # return all(col.lower() in split_col for col in desired_col.split('_'))

    def _get_indices(self, header_columns, status, soc_col, state_col):
        """
        return indices value of status, occupation and state columns
        """
        col_dict = {
                'status': ['CASE_STATUS', 'STATUS'], 
                'occ': ['SOC_NAME', 'LCA_CASE_SOC_NAME'],
                'state': ['WORKSITE_STATE', 'LCA_CASE_WORKLOC1_STATE']}
        try:
            # loop through all column names 
            for i, split_col in enumerate(header_columns):
                split_col = split_col.lower()
            #     for col in col_dict['status']:
            #         if col.lower() in split_col:
            #             status_index = i
            #     for col in col_dict['occ']:
            #         if col.lower() in split_col:
            #             occ_index = i
            #     for col in col_dict['state']:
            #         if col.lower() in split_col:
            #             state_index = i




                if status.lower() in split_col:
                    status_index = i
                if 'soc' in split_col:
                    if 'name' in split_col:
                        occ_index = i
                if 'worksite' in split_col:
                    if 'state' in split_col:
                        state_index = i
                elif 'workloc1' in split_col:
                    if 'state' in split_col:
                        state_index = i
            return status_index, occ_index, state_index
        # handle exception
        except UnboundLocalError:
            raise Exception('COLUMN NAME NOT FOUND. PLEASE PASS IN ')
        except IndexError:
            raise Exception('COLUMN NAMES NOT FOUND. PLEASE CHECK COLUMN NAMES')

    def write_to_file(self, top, filename, col2='NUMBER_CERTIFIED_APPLICATIONS', col3='PERCENTAGE'):
        """
        Saves output to output_filename
        Args:
            top (list): top N list of tuples [(desired_col, counts), ...]
            filename (str): filepath where to save output 
            col2 (str): Name of counts column 
            col3 (str): Name of percentage column
        """
        # get column nam from passed in output file name 
        name = filename.split('_')[-1].split('.')[0].upper()
        with open(filename, 'w') as f:
            # write column names
            f.write('TOP_{}'.format(name) + self.delimiter + \
                    col2  + self.delimiter + col3 + '\n')
            # write data 
            for line in top:
                line = self.delimiter.join(map(str, line))
                f.write(line + '\n')
    
