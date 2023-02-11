import argparse
import csv


def round_value_to_near_grade(value, grades):
    """
    >>> grades = [1.0, 1.3, 1.7]
    >>> round_value_to_near_grade(0.9, grades)
    1.0
    >>> round_value_to_near_grade(1.1, grades)
    1.0
    >>> round_value_to_near_grade(1.2, grades)
    1.3
    >>> round_value_to_near_grade(2.1, grades)
    1.7
    >>> round_value_to_near_grade(1.5, grades)
    1.3
    """
    if value <= grades[0]:
        return grades[0]
    if grades[-1] <= value:
        return grades[-1]

    # case: value in grades
    for index, grade in enumerate(grades):
        if value >= grade:
            break
    if (value - grades[index]) <= (grades[index + 1] - value):
        return grades[index]
    else:
        return grades[index + 1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prediction_csv")
    parser.add_argument("target_facet_csv")
    parser.add_argument("rounded_csv")
    args = parser.parse_args()

    with open(args.prediction_csv) as fin:
        reader = csv.DictReader(fin)
        rows = list(reader)
    with open(args.target_facet_csv) as fin:
        reader = csv.Reader(fin)
        grades = [float(row[0]) for row in reader]

    # TODO: ここから
