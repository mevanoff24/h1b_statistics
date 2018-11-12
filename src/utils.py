def sort_values(counts, top_N=10):
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


def add_percentage(top, N):
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