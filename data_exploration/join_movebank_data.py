import pandas as pd
import os

data_path = os.path.join('data', 'movebank')

studies = pd.read_csv(os.path.join(data_path, 'gps_studies.csv'))
deployments = pd.read_csv(os.path.join(data_path, 'deployments.csv'))
individuals = pd.read_csv(os.path.join(data_path, 'gps_individuals.csv'))

studies.head()

study_cols = ['id', 'name', 'taxon_ids', 'main_location_lat', 'main_location_long', 'timestamp_first_deployed_location', 'timestamp_last_deployed_location'
    , 'number_of_deployments', 'number_of_deployed_locations', 'number_of_individuals', 'number_of_tags', 'study_objective'
    , 'license_terms', 'suspend_license_terms', 'sensor_type_ids', 'is_test']

deployments.head()

deployment_cols = ['id','study_id','animal_life_stage','animal_mass','animal_reproductive_condition','deploy_off_latitude','deploy_off_longitude','deploy_off_timestamp','deploy_on_latitude',
                   'deploy_on_longitude',
                   'deploy_on_timestamp','deployment_end_comments','deployment_end_type','geolocator_light_threshold','geolocator_sun_elevation_angle']

individuals.head()

individual_columns = ['id','nick_name','sex','taxon_canonical_name','timestamp_start','timestamp_end','number_of_events','number_of_deployments','taxon_detail','sensor_type_ids','study_id']