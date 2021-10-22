import pandas as pd
import os
from api.movebank.util import movebankAPI
from api.movebank.call import getMoveBankData
from argparse import ArgumentParser

# always execute scripts using __name__ == '__main__'
if __name__ == '__main__':

    # parse arguments from run profile
    parser = ArgumentParser()
    parser.add_argument('--study_id', required=False)
    parser.add_argument('--individual_id', required=False)
    parser.add_argument('--sensor_id', required=False)
    args = parser.parse_args()

    # set out path
    out_path = os.path.join('../data', 'movebank')

    # make directory for files if none exists
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    mbapi = movebankAPI()
    gmbd = getMoveBankData()

    print('getting joined data...')

    joined_data = pd.read_csv(os.path.join(out_path,'_joined_data.csv'))

    temp = joined_data.sort_values('number_of_events', ascending=False).loc[0,['study_id', 'individual_id']]

    study_id = temp.study_id if not args.study_id else args.study_id
    individual_id = temp.individual_id if not args.individual_id else args.individual_id
    sensor_id = 653 if not args.sensor_id else args.sensor_id

    # EVENTS

    print('pulling events...')

    file_name = f'gps_events_s{study_id}_i{individual_id}_ss{sensor_id}.csv'
    print(f'\t{file_name}')
    # gps_sensor_id = 653
    ids = []
    temp = [(study_id, individual_id, sensor_id)]
    ids.extend(temp)
    gps_events_temp = gmbd.mulitprocess_api_call(func=mbapi.getIndividualEvents, values=ids)
    gps_events = [response for response in gps_events_temp if response]
    empty_count = len(gps_events_temp) - len(gps_events)
    print(f'\t\tgot {len(gps_events)} gps_events - {empty_count} were empty')
    [gmbd.write_to_csv(event, file_name, out_path) for event in gps_events]