from decimal import Decimal


def format_dict_str(record):
    """
    Transform all dict values into strings
    """
    for key, value in record.items():
        record[key] = str(value)
    return record


def dec2float(row):
    """
    Checks all items of dictionary and converts Decimal types to float
    """
    for key, value in row.items():
        if isinstance(value, type(Decimal())):
            row[key] = float(value)

    return row