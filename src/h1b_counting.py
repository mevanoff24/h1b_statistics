import csv
import operator
from argparse import ArgumentParser

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
        
        
    def compute_counts(self, certified_value='CERTIFIED', status='STATUS'):
        """
        Computes counts for desired column field based on column names 
        Args:
            param1 (int): The first parameter.
            param2 (:obj:`str`, optional): The second parameter. Defaults to None.
                Second line of description should be indented.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            counts (dict): dictionary of {desired_col : count}
            N (int): total number of certified applications regardless of occupation
        """
        occupation_counts = {}
        state_counts = {}
        with open(self.input_filename, 'r') as f:
            # read file 
            lines = csv.reader(f, quotechar=self.quotechar, delimiter=self.delimiter,
                             quoting=csv.QUOTE_ALL)
            # get column names
            columns = next(lines)
            status_index, occ_index, state_index = self._get_indices(columns, status=status)
            # get total number of certified applications regardless of occupation
            N = 0
            for line in lines:
                # only if status == CERTIFIED
                if line[status_index] == certified_value:
                    occ = line[occ_index]
                    state = line[state_index]
                    N += 1
                    # increment count based on occupation
                    if occ not in occupation_counts:
                        occupation_counts[occ] = 0
                    occupation_counts[occ] += 1
                    # increment count based on state
                    if state not in state_counts:
                        state_counts[state] = 0
                    state_counts[state] += 1
                    
        # return count dicts and total number of certified applications regardless of occupation
        return occupation_counts, state_counts, N

    def _get_indices(self, header_columns, status):
        """
        return indices value of status, occupation and state columns
        """
        for i, split_col in enumerate([col.split('_') for col in header_columns]):
            for split in split_col:
                # UPDATE 
                if status in split:
                    status_index = i
                # handles both `SOC_NAME` and `LCA_CASE_SOC_NAME`
                if 'SOC' and 'NAME' in split:
                    occ_index = i
                # handles both `EMPLOYER_STATE` and `LCA_CASE_EMPLOYER_STATE`
                if 'EMPLOYER' and 'STATE' in split:
                    state_index = i
        return status_index, occ_index, state_index

    def sort_values(self, counts, top_N=10):
        """
        Sorts `counts` to return `top_N` columns and counts 
        Args:
            counts (dict): Count dictionary
            top_N (int): Number of top columns 
        
        Returns:
            top (list): top N list of tuples [(desired_col, counts), ...]
        """
        top = sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:top_N]
        return top
    
    def add_percentage(self, top, N):
        """
        Add percentage of applications that have been certified compared 
        to total number of certified applications regardless of state. 
        Args:
            top (list): top N list of tuples [(desired_col, counts), ...]
            N (int): total number of certified applications regardless of occupation
        
        Returns:
            (list): top N list of tuples [(desired_col, counts, percentage), ...]
        """
        print([top[i] + (((str(round((top[i][1] / N) * 100, 1)) + '%'),)) for i in range(len(top))])
        return [top[i] + (((str(round((top[i][1] / N) * 100, 1)) + '%'),)) for i in range(len(top))]
    
    def write_to_file(self, top, filename, col2='NUMBER_CERTIFIED_APPLICATIONS', col3='PERCENTAGE'):
        """
        Saves output to output_filename
        Args:
            top (list): top N list of tuples [(desired_col, counts), ...]
        """
        name = filename.split('_')[-1].split('.')[0].upper()
        with open(filename, 'w') as f:
            # UPDATE 
            f.write('TOP_{}'.format(name) + self.delimiter + \
                    col2  + self.delimiter + col3 + '\n')
            for line in top:
                line = self.delimiter.join(map(str, line))
                f.write(line + '\n')
        

def main():
    parser = ArgumentParser()

    parser.add_argument('input_filename', help='read CSV file from input_filename', type=str, metavar='FILE 1')
    parser.add_argument('occupation_output_filename', help='write report to occupation_output_filename', 
                        type=str, metavar='FILE 2')
    parser.add_argument('state_output_filename', help='write report to state_output_filename', 
                        type=str, metavar='FILE 3')
    parser.add_argument('-topN', '--topN', help='number of top occurances -- default(10)', type=int, default=10)
    args = parser.parse_args()
    print(args)

    top_model = TopCounts(input_filename=args.input_filename, 
                               occupation_output_filename=args.occupation_output_filename,
                               state_output_filename=args.state_output_filename, 
                               delimiter=';')

    occ_counts, state_counts, N = top_model.compute_counts(certified_value='CERTIFIED')

    top_occs = top_model.sort_values(occ_counts, top_N=args.topN)
    top_states = top_model.sort_values(state_counts, top_N=args.topN)
    top_occs = top_model.add_percentage(top_occs, N)
    top_states = top_model.add_percentage(top_states, N)
    top_model.write_to_file(top_occs, top_model.occupation_output_filename)
    top_model.write_to_file(top_states, top_model.state_output_filename)

if __name__ == '__main__':
    main()
    

