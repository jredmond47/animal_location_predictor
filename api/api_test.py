import csv, os, datetime
from argparse import ArgumentParser
from functools import partial
from api_util import movebankAPI
from multiprocessing import Pool


def write_to_csv(data:list, out_file_name:str):
    '''
    write data to csv - create new file if none exists, append if it does
    :param data:
    :param out_file_name:
    :return:
    '''
    out_path = os.path.join('data', 'api_test', out_file_name)
    if len(data) > 0:
        fieldnames = list(data[0].keys())
        file_exists = os.path.isfile(out_path)
        if file_exists:
            with open(out_path, 'a', encoding="utf-8", newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writerows(data)
        else:
            with open(out_path, 'w', encoding="utf-8", newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
    else:
        print(f'''No data pertaining to {out_file_name.replace('.csv','')}''')


# always execute scripts using __name__ == '__main__'
if __name__ == '__main__':

    # parse arguments from run profile
    parser = ArgumentParser()
    parser.add_argument('--study-id',default=7006760) # study id for Costa Lab Northern Elephant Seals
    parser.add_argument('--individual-id',default=-1)
    parser.add_argument('--sensor-type-id',default=-1)
    parser.add_argument('--delete-files',default=True)
    args = parser.parse_args()

    # set out path
    out_path = os.path.join('data','api_test')

    # delete existing files if appropriate
    if args.delete_files and os.path.exists(out_path):
        for file in os.listdir(out_path):
            os.remove(os.path.join(out_path,file))

    # make directory for files if none exists
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    mbapi = movebankAPI()

    allstudies = mbapi.getStudies()
    write_to_csv(allstudies, 'studies.csv')

    gpsstudies = mbapi.getStudiesBySensor(allstudies, 'GPS')
    write_to_csv(gpsstudies, 'gps_studies.csv')

    # parallelize the data pull for the individuals
    pool = Pool(16)
    gps_study_ids = [s['id'] for s in gpsstudies]
    s = datetime.datetime.now()
    individuals = pool.map(mbapi.getIndividualsByStudy, gps_study_ids)
    print(f'Elapsed Time for getting individuals: {datetime.datetime.now() - s}')
    wtc_partial = partial(write_to_csv, out_file_name='gps_study_individuals.csv')
    pool.map(wtc_partial, individuals)

    # gpsevents = mbapi.getIndividualEvents(study_id=9493874, individual_id=11522613,
    #                                       sensor_type_id=653)  # GPS events
    # if len(gpsevents) > 0:
    #     mbapi.prettyPrint(mbapi.transformRawGPS(gpsevents))
    #
    # # Print tri-axial acceleration in m/s^2: [(ts, deployment, accx, accy, accz), [ts,...],...]
    # accevents = mbapi.getIndividualEvents(study_id=9493874, individual_id=11522613,
    #                                       sensor_type_id=2365683)  # ACC events
    # if len(accevents) > 0:
    #     mbapi.prettyPrint(mbapi.transformRawACC(accevents))