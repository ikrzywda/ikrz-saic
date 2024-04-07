import pandas as pd

def compute_intersection(Ku, dupa):
    """
    Compute intersection point between two curves represented by lists of x and y coordinates.
    
    Args:
    - Ku: List of tuples (x, y) representing the first curve.
    - dupa: List of tuples (x, y) representing the second curve.
    
    Returns:
    - intersection_point: Tuple (x, y) representing the intersection point.
    """
    for i in range(len(Ku) - 1):
        x1, y1 = Ku[i]
        x2, y2 = Ku[i + 1]
        for j in range(len(dupa) - 1):
            x3, y3 = dupa[j]
            x4, y4 = dupa[j + 1]
            denom = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
            if denom != 0:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
                if 0 <= t <= 1 and 0 <= u <= 1:
                    x_intersect = x1 + t * (x2 - x1)
                    y_intersect = y1 + t * (y2 - y1)
                    return x_intersect, y_intersect
    return None

def main():
    # Load data from CSV using pandas
    data = pd.read_csv('data.csv')
    
    # Extract relevant columns
    Ku = list(zip(data['freq'], data['Ku [dB]']))
    dupa = list(zip(data['freq'], data['dupa']))
    
    # Compute intersection point
    intersection_point = compute_intersection(Ku, dupa)
    if intersection_point:
        print("Intersection point:", intersection_point)
    else:
        print("No intersection point found.")

if __name__ == "__main__":
    main()
