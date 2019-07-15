import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler('instacart_order_count.log')
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


def read_file(input_file):
    """
        Read line from the input file
        :param input_file: input file name
        :return: Single line at a time from the file
    """
    try:
        with open(input_file, 'r') as fd:
            next(fd)
            for line in fd:
                yield(line)
    except IOError:
        print("Could not read file",input_file)


def ingest_products(lines):
    """
        Ingest input file products.csv to prod_dept dictionary
        :param lines: Line from the file
        :return: prod_dept
    """
    prod_dept = {}
    for line in lines:
        try:
            columns = line.strip().split(',')
            product_id = columns[0]
            department_id = columns[3]
            prod_dept[product_id] = int(department_id.strip())
        except:
            logger.exception("No department_id found for product.Skipping line with invalid data ")
            continue
    return(prod_dept)

def ingest_orders(lines):
    """
        Ingest input file order_products.csv to dept dictionary
        :param lines: Line from the file
        :return: dept_check
    """
    dept = {}
    for line in lines:
        try:
            columns = line.strip().split(',')
            product_id = columns[1]
            reordered = columns[3]


            department_id = prod_dept.get(product_id, None)
            if department_id is None:
                logger.exception("Skipping line with invalid data ")
                continue



        except:
            logger.exception("Skipping line with invalid data ")
            continue

        # To check if an entry for department_id is present in the dept dictionary
        dept_check = dept.get(department_id, None)

        # Initialize the department id when it is coming for the first time
        if dept_check is None:
            dept[department_id] = {'first_time': 0, 'total': 0}

        try:
            dept[department_id]['total'] = int(dept.get(department_id, {}).get('total')) + 1
        except:
            logger.exception("Skipping line with invalid data ")
            continue
        try:
            if int(reordered) == 0:
                dept[department_id]['first_time'] = int(dept.get(department_id, {}).get('first_time')) + 1
        except:
            logger.exception("Skipping line with invalid data ")
            continue

    return(dept)

def calculate_percentage(dept):
    """
        Calculate percentage of requests
        :param dept: dept dictionary with key department_id
        :return: dept : dept dictionary with key department_id after adding percentage
    """
    # Calculate percentage and round off to 2 decimal
    for key in dept.keys():
        dept[key]['ratio'] = round(float(dept[key]['first_time']) / float(dept[key]['total']),2)

    return(dept)

def write_output(dept,file_fd):
    """
        Ingest input file order_products.csv to dept dictionary
        :param dept: dept dictionary
        :param fd : file handler for output file
        :return: dept_check
    """
    header='department_id, number_of_orders, number_of_first_orders, percentage'+'\n'
    file_fd.write(header)
    for key in sorted(dept):
        if dept[key]['total'] ==0 :
            continue
        report = str(key) + ',' + str(dept[key]['total']) + ',' + str(dept[key]['first_time']) + ',' + str(dept[key]['ratio'])+ '\n'
        file_fd.write(report)

def file_open(output_file):
    """
        Ingest input file order_products.csv to dept dictionary
        :param output_file : output filename
        :return: file handler of the output file
    """
    fh = open(output_file, 'w')
    return fh

def file_close(fh):
    """
        Ingest input file order_products.csv to dept dictionary
        :param output_file : file handler of output file
        :return: None
    """
    fh.close()

if __name__ == '__main__':

    input_file_product = sys.argv[1]
    input_file_orders = sys.argv[2]
    output_file = sys.argv[3]


    # Open input file products.csv
    input_file_product_fd = read_file(input_file_product)

    # Ingest input file products.csv to a dictionary
    prod_dept= ingest_products(input_file_product_fd)

    # Open input file order_products.csv
    input_file_orders_fd = read_file(input_file_orders)

    # Ingest input file order_products.csv. For each product in order_products.csv lookup department from products.csv
    dept = ingest_orders(input_file_orders_fd)

    # Calculate percentage from first time order and total number of orders
    dept = calculate_percentage(dept)

    # Open output file
    output_file_fd=file_open(output_file)

    # Write into report.csv
    write_output(dept,output_file_fd)

    # Close output file
    file_close(output_file_fd)





