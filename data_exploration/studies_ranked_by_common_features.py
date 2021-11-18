import sys, os
sys.path.append("/Users/branpham/Documents/gt/Animal Tracking/animal_tracking/")
import pandas as pd
from api.movebank.util import movebankAPI
from api.movebank.call import getMoveBankData


if __name__ == '__main__':

    mbapi = movebankAPI()
    gmbd = getMoveBankData()

    # get study ids for all studies
    all_studies = mbapi.getStudies()
    os.chdir("/Users/branpham/Documents/gt/Animal Tracking/animal_tracking/")
    out_path = os.path.join('../data', 'movebank')
    all_studies_df = pd.DataFrame(all_studies)
    print(len(all_studies_df))
    # remove studies that are not available for free use
    studies = all_studies_df[all_studies_df['license_terms'] == '']
    print(len(studies))
    # select studies that include GPS sensors
    studies = studies[studies['sensor_type_ids'].str.contains("GPS")]
    print(len(studies))
    # get top 100 studies with deployed locations
    top_studies = studies.sort_values(by=['number_of_deployed_locations'])[:19]
    all_study_ids = top_studies['id'].unique()

    event_data = []
    # get features for all studies
    for study_id in all_study_ids:
        # get all individuals per study
        individual_ids = gmbd.mulitprocess_api_call(func=mbapi.getIndividualsByStudy, values=[study_id])
        if not individual_ids["__is_empty__"]:
            curr_df = pd.DataFrame(individual_ids)
            
            # pull all columns and its populated percentage
            # add any new columns to ongoing list
            # create a dictionary for this study id with its columns and percentages
            event_data.append(individual_ids)

        # features_all = []
        # ids = []
        # temp = [(study_id, individual_id, sensor_id)]
        # ids.extend(temp)
        # gps_events_temp = gmbd.mulitprocess_api_call(func=mbapi.getIndividualEvents, values=ids)
        # gps_events = [response for response in gps_events_temp if response]
        # empty_count = len(gps_events_temp) - len(gps_events)
        # print(f'\t\tgot {len(gps_events)} gps_events - {empty_count} were empty')
        # [gmbd.write_to_csv(event, file_name, out_path) for event in gps_events]

    # file_name = f'all_studies.csv'
    # [gmbd.write_to_csv(study, file_name, out_path) for study in all_studies]




