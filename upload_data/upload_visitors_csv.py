from env_var import get_env_var
from csv_util import read_csv_file
import datetime
from cloud_storage_util import set_credentials_json, upload_blob


def get_env_vars():
    global credentials_json_path
    global visitors_data_bucket_name

    credentials_json_path = get_env_var('SERVICE_ACCOUNT_CREDENTIALS_JSON')
    if credentials_json_path == '':
        return False

    visitors_data_bucket_name = get_env_var('NEWGARDEN_VISITORS_DATA_BUCKET')
    if visitors_data_bucket_name == '':
        return False

    # success
    return True


def parse_arguments():
    import argparse
    global csv_file_name

    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file_name', help='csv file name.')

    args = parser.parse_args()
    csv_file_name = args.csv_file_name

    if csv_file_name is None:
        print('parse_arguments: csv_file_name is missing.')
        return False

    # success
    return True


def main():
    print('\nStarting upload_visitors_csv.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print(f'credentials_json_path: {credentials_json_path}')
    print(f'visitors_data_bucket_name: {visitors_data_bucket_name}')

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('Args:')
    print(f'csv_file_name: {csv_file_name}')

    # debug: read and print data rows
    data_rows = read_csv_file(csv_file_name)
    print('data_rows:')
    print(data_rows)

    today = datetime.date.today()
    destination_blob_name = str(today) + "/" + csv_file_name
    print(f'destination_blob_name: {destination_blob_name}')

    set_credentials_json(credentials_json_path)
    success = upload_blob(visitors_data_bucket_name, csv_file_name, destination_blob_name)
    if not success:
        print('upload_blob failed.  Exit.')
        return


if __name__ == '__main__':
    main()

