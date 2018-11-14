from argparse import ArgumentParser

from top_counts import TopCounts
from utils import sort_values, add_percentage



def main():
    parser = ArgumentParser()
    parser.add_argument('input_filename', help='read CSV file from input_filename', type=str, metavar='FILE 1')
    parser.add_argument('occupation_output_filename', help='write report to occupation_output_filename', 
                        type=str, metavar='FILE 2')
    parser.add_argument('state_output_filename', help='write report to state_output_filename', 
                        type=str, metavar='FILE 3')
    parser.add_argument('-topN', '--topN', help='number of top occurances -- default(10)', type=int, default=10)
    parser.add_argument('-c', '--status_level', help='STATUS LEVEL -- default(CERTIFIED)', type=str, default='CERTIFIED')
    parser.add_argument('-a', '--status_column', help='STATUS COLUMN NAME -- default(STATUS)', type=str, default='STATUS')
    parser.add_argument('-o', '--occupation_column', help='OCCUPATION COLUMN NAME -- default(SOC_NAME)', type=str, default='SOC_NAME')
    parser.add_argument('-s', '--state_column', help='STATE COLUMN NAME -- default(WORKSITE_STATE)', type=str, default='WORKSITE_STATE')
    args = parser.parse_args()
    # initialize model 
    top_model = TopCounts(input_filename=args.input_filename, 
                               occupation_output_filename=args.occupation_output_filename,
                               state_output_filename=args.state_output_filename, 
                               delimiter=';')
    # compute counts 
    occ_counts, state_counts, N = top_model.compute_counts(certified_value=args.status_level, 
                                status=args.status_column, soc_col=args.occupation_column, 
                                state_col=args.state_column)
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
    

