import os
import subprocess
from glob import glob
import logging

import dateutil.parser

from data_utilities.data_access_layer import DataAccessLayer
from import_scripts.add_calculated_distances_to_db import update_position_info
from import_scripts.add_routes import create_routes_for_date
from import_scripts.transform_raw_data import process_raw_data

logging.basicConfig(level=logging.DEBUG)
from logging import getLogger

log = getLogger('data_import')

helo_root = os.path.expanduser('~/git-repos/helo')
data_root = os.path.join(helo_root, 'data')
scripts_root = os.path.join(helo_root, 'import_scripts')
os.chdir(data_root)
zip_files = glob('*.zip')
csv_files = glob('*.csv')
unprocessed_files = sorted(set(zip_files) - set(f.replace('.csv', '') for f in csv_files))
log.info('Number of unprocessed files: %s', len(unprocessed_files))

for new_file in unprocessed_files:
    log.info('Extracting helicopter data from zip file: %s', new_file)
    return_code = subprocess.call([os.path.join(scripts_root, 'process_file.sh'),
                                   new_file])
    if not return_code == 0:
        log.warning('Extraction of file failed with return code: %s', return_code)

    log.info('Truncating raw_data table')
    dal = DataAccessLayer()
    dal.engine.execute('truncate raw_data')
    dal.session.commit()

    log.info('Loading %s into the database.', new_file+'.csv')
    return_code = subprocess.call([os.path.join(scripts_root, 'copy_and_add.sh'), new_file + '.csv'])

    if not return_code == 0:
        log.warning('Adding file data to database failed with return code: %s', return_code)

    log.info('Normalising raw data')
    process_raw_data()

    file_date = dateutil.parser.parse(new_file.replace('.zip',''))
    log.info('Adding derived position data for date: %s', file_date)
    update_position_info(file_date)

    log.info('Finding routes for date: %s', file_date)
    create_routes_for_date(file_date)