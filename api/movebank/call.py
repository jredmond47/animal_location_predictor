import csv, os
from argparse import ArgumentParser
import tqdm
from api.movebank.util import movebankAPI
from multiprocessing import Pool


class getMoveBankData():

    def write_to_csv(self, data: list, out_file_name: str, out_path: str):
        '''
        write data to csv - create new file if none exists, append if it does
        :param data:
        :param out_file_name:
        :return:
        '''
        destination = os.path.join(out_path, out_file_name)
        if len(data) > 0:
            file_exists = os.path.isfile(destination)
            column_names = list(data[0].keys())
            if file_exists:
                with open(destination, 'a', encoding="utf-8", newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=column_names)
                    writer.writerows(data)
            else:
                with open(destination, 'w', encoding="utf-8", newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=column_names)
                    writer.writeheader()
                    writer.writerows(data)
        else:
            print(f'''No data pertaining to {out_file_name.replace('.csv', '')}''')

    def write_to_txt(self, data: str, out_file_name, out_path):
        '''

        :param data:
        :param out_file_name:
        :return:
        '''
        destination = os.path.join(out_path, out_file_name)
        with open(destination, 'w', encoding="utf-8") as txt_file:
            txt_file.write(data)

    def mulitprocess_api_call(self, func, values):
        pool = Pool(3)

        responses = []
        print('\t\t', end='')
        for response in tqdm.tqdm(pool.imap_unordered(func, values), total=len(values)):
            responses.append(response)

        return responses


# always execute scripts using __name__ == '__main__'
if __name__ == '__main__':

    # parse arguments from run profile
    parser = ArgumentParser()
    parser.add_argument('--delete-files', default=False, action='store_true')
    parser.add_argument('--get-events', default=False, action='store_true')
    args = parser.parse_args()

    # set out path
    out_path = os.path.join('../data', 'movebank')

    # delete existing files if appropriate
    if args.delete_files and os.path.exists(out_path):
        for file in os.listdir(out_path):
            os.remove(os.path.join(out_path, file))

    # make directory for files if none exists
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    mbapi = movebankAPI()
    gmbd = getMoveBankData()

    print('Pulling...')

    # DATA ATTRIBUTES
    file_name = 'data_attributes.txt'
    print(f'\t{file_name}')
    data_attributes = mbapi.callMovebankAPI(('attributes'))
    gmbd.write_to_txt(data_attributes, file_name, out_path)

    # SENSOR DATA
    file_name = 'sensors.csv'
    print(f'\t{file_name}')
    sensor_info = mbapi.getSensors()
    gmbd.write_to_csv(sensor_info, file_name, out_path)

    # ALL STUDIES
    file_name = 'studies.csv'
    print(f'\t{file_name}')
    allstudies = mbapi.getStudies()
    gmbd.write_to_csv(allstudies, file_name, out_path)

    # DEPLOYMENTS
    file_name = 'deployments.csv'
    print(f'\t{file_name}')
    deployments_temp = gmbd.mulitprocess_api_call(func=mbapi.getDeploymentsByStudy, values=[s['id'] for s in allstudies])
    deployments = [response for response in deployments_temp if not response[0]['__is_empty__']]
    deployments_empty = [response for response in deployments_temp if response[0]['__is_empty__']]
    print(f'\t\tgot {len(deployments)} deployments - {len(deployments_empty)} were empty')
    [gmbd.write_to_csv(deployment, file_name, out_path) for deployment in deployments]
    [gmbd.write_to_csv(deployment, f'empty_{file_name}', out_path) for deployment in deployments_empty]

    # GPS STUDIES
    file_name = 'gps_studies.csv'
    print(f'\t{file_name}')
    gps_studies = mbapi.getStudiesBySensor(allstudies, 'GPS')
    gmbd.write_to_csv(gps_studies, file_name, out_path)

    # INDIVIDUALS
    file_name = 'gps_individuals.csv'
    print(f'\t{file_name}')
    gps_individuals_temp = gmbd.mulitprocess_api_call(func=mbapi.getIndividualsByStudy, values=[s['id'] for s in gps_studies])
    gps_individuals = [response for response in gps_individuals_temp if not response[0]['__is_empty__']]
    gps_individuals_empty = [response for response in gps_individuals_temp if response[0]['__is_empty__']]
    print(f'\t\tgot {len(gps_individuals)} gps_individuals - {len(gps_individuals_empty)} were empty')
    [gmbd.write_to_csv(individual, file_name, out_path) for individual in gps_individuals]
    [gmbd.write_to_csv(individual, f'empty_{file_name}', out_path) for individual in gps_individuals_empty]

    # EVENTS
    if args.get_events:
        file_name = 'gps_events.csv'
        print(f'\t{file_name}')
        gps_sensor_id = 653
        ids = []
        for individual in gps_individuals:
            temp = [(i['study_id'], i['individual_id'], gps_sensor_id) for i in individual]
            ids.extend(temp)
        gps_events_temp = gmbd.mulitprocess_api_call(func=mbapi.getIndividualEvents, values=ids)
        gps_events = [response for response in gps_events_temp if response]
        empty_count = len(gps_events_temp) - len(gps_events)
        print(f'\t\tgot {len(gps_events)} gps_events - {empty_count} were empty')
        [gmbd.write_to_csv(event, file_name, out_path) for event in gps_events]