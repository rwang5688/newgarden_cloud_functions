import os
import datetime
from csv_util import read_csv_file
from cloud_storage_util import upload_blob


def get_env_var(env_var_name):
    env_var = ''
    if env_var_name in os.environ:
        env_var = os.environ[env_var_name]
    else:
        print(f'get_env_var: Failed to get {env_var_name}.')
    return env_var


def get_env_vars():
    global csv_bucket_name
    global credentials_json

    csv_bucket_name = get_env_var('NEWGARDEN_VISITORS_CSV_DATA_BUCKET')
    if csv_bucket_name == '':
        return False

    credentials_json = get_env_var('NEWGARDEN_CLOUD_FUNCTIONS_CREDENTIALS_JSON')
    if credentials_json == '':
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
    print(f'csv_bucket_name: {csv_bucket_name}')
    print(f'credentials_json: {credentials_json}')

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('Args:')
    print(f'csv_file_name: {csv_file_name}')

    # debug: print CSV file rows
    rows = read_csv_file(csv_file_name)
    print('CSV file rows:')
    print(rows)

    today = datetime.date.today()
    destination_blob_name = str(today) + "/" + csv_file_name
    print(f'destination_blob_name: {destination_blob_name}')

    success = upload_blob(credentials_json, csv_bucket_name, csv_file_name, destination_blob_name)
    if not success:
        print('upload_blob failed.  Exit.')
        return


if __name__ == '__main__':
    main()

