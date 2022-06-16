"""THis class collects the meta.json files in each wav file and combines into a single csv file,cause csv file in the
original dataset doesn't contain all audio files information ,it also cleans the csv file  """
import os
import glob

import numpy as np
import pandas as pd


class CombinedCsv:

    """
    this function creates csv collecting the path of each type of audio file
    """

    @staticmethod
    def create_csv():

        try:
            dataset_path = '../Extracted_data'
            global frame
            directories = list(set(map(os.path.basename, glob.glob('{}/202*'.format(dataset_path)))))
            list_data, source_path, direct, heavy_cough, shallow_cough, shallow_breath, fast_counting, vowel_o, vowel_e = (
                [] for i in range(9))
            for d in directories:
                print(d)
                path_ = '{}/{}/'.format(dataset_path, d)
                for dir in os.listdir(path_):
                    path_dir = '{}/{}/{}'.format(dataset_path, d, dir)
                    isdir = os.path.isdir(path_dir)
                    if isdir:
                        paths = ['metadata.json', 'cough-shallow.wav', 'cough-heavy.wav', 'breathing-shallow.wav',
                                 'counting-fast.wav', 'vowel-e', 'vowel-o']
                        if ([os.path.isfile(f) for f in paths]):
                            print("ok")
                            path_direct = '{}/{}/{}/metadata.json'.format(dataset_path, d, dir)
                            with open(path_direct, encoding="utf8") as f:
                                print(f)
                                source_path.append(path_direct)
                                direct.append(dir)
                                heavy_cough.append('{}/{}/{}/cough-heavy.wav'.format(dataset_path, d, dir))
                                shallow_cough.append('{}/{}/{}/cough-shallow.wav'.format(dataset_path, d, dir))
                                shallow_breath.append('{}/{}/{}/breathing-shallow.wav'.format(dataset_path, d, dir))
                                fast_counting.append('{}/{}/{}/counting-fast.wav'.format(dataset_path, d, dir))
                                vowel_o.append('{}/{}/{}/vowel-o.wav'.format(dataset_path, d, dir))
                                vowel_e.append('{}/{}/{}/vowel-e.wav'.format(dataset_path, d, dir))
                                data = pd.read_json(f, typ='series')
                            list_data.append(data)
                            frame = pd.concat(list_data, axis=1, ignore_index=True)
                    else:
                        print("meta file not found")

            dframe = frame.T
            dframe['id'] = direct
            dframe['source'] = source_path
            dframe['h_cough'] = heavy_cough
            dframe['s_cough'] = shallow_cough
            dframe['s_breath'] = shallow_breath
            dframe['F_count'] = fast_counting
            dframe['vowel_E'] = vowel_e
            dframe['vowel_O'] = vowel_o
            print(dframe)
            csvfile = dframe.to_csv('All_data.csv', encoding='utf-8', index=False)
            return csvfile

        except:
            print("some error occurred when creating csv file")

    """
    this function fills the missing values in the dataframe 
    """

    def fill_missing_values(self, csv):
        a = csv.isnull().sum() / len(csv) * 100
        variables = csv.columns
        variable = []
        for i in range(csv.columns.shape[0]):
            if a[i] <= 40:  # setting the threshold as 40%
                variable.append(variables[i])
        # creating a new dataframe using the above variables
        new_data = csv[variable]
        # filling the missing values with most frequent values
        cols = ["rU"]
        new_data[cols] = new_data[cols].fillna(new_data.mode().iloc[0])
        print(new_data.isnull().sum() / len(new_data) * 100)
        return new_data

    """
    this function removes unncessary columns in the dataframe
    """

    def remove_unnecessary_columns(self, unfiltered_csv):
        # removing unnecessary columns or meaningless ones
        print(unfiltered_csv.drop(['dT', 'l_l', 'fV'], 1, inplace=True))

        unfiltered_csv.dropna(axis=0, inplace=True)
        print(unfiltered_csv.isnull().sum() / len(unfiltered_csv) * 100)
        print(unfiltered_csv.shape)

        # finding any outliers accoring to age of users
        min_thresold, max_thresold = unfiltered_csv.a.quantile([0.001, 0.999])
        print(min_thresold, max_thresold)

        print(unfiltered_csv[unfiltered_csv.a < min_thresold])
        print(unfiltered_csv[unfiltered_csv.a > max_thresold])

        unfiltered_csv = unfiltered_csv[(unfiltered_csv.a > min_thresold) & (unfiltered_csv.a < max_thresold)]
        print(unfiltered_csv.shape)

        unfiltered_csv['a'] = np.where(unfiltered_csv['a'] >= max_thresold,
                                       max_thresold,
                                       np.where(unfiltered_csv['a'] <= min_thresold,
                                                min_thresold,
                                                unfiltered_csv['a']))

        # checking for any duplicates-didn't find any duplicates
        bool_series = unfiltered_csv.duplicated()
        print(bool_series.value_counts())
        print(type(unfiltered_csv))

        return unfiltered_csv

    """
    this function renames the target lables to binary negative and positive in the dataframe
    mild positive are taken as positive 
    and the data imbalanced is found
    """

    def rename_target_labels(self, clean_csv):
        # replacing covid status with negative and positive
        clean_csv["covid_status"].replace(
            {"no_resp_illness_exposed": "Negative", "healthy": "Negative", "resp_illness_not_identified": "Negative",
             "recovered_full": "Negative"}, inplace=True)
        clean_csv["covid_status"].replace(
            {"positive_moderate": "Positive", "positive_mild": "Positive", "positive_asymp": "Positive"}, inplace=True)
        print(clean_csv['covid_status'][1:5])

        print(clean_csv["covid_status"].value_counts())  # imbalanced data

        return clean_csv

    """
    this function saves the cleaned dataframe into a csv file for future use
    """

    def save_the_filtered_csv(self, y_labels):
        csvfile = y_labels.to_csv('combine_data.csv', encoding='utf-8', index=False)
        return csvfile

    """
    this function merges the above function to clean the csv file 
    """

    @staticmethod
    def clean_csv(self):
        csv = pd.read_csv('./All_data.csv')
        unfiltered_csv = self.fill_missing_values(csv)
        clean_csv = self.remove_unnecessary_columns(unfiltered_csv)
        y_lables = self.rename_target_labels(clean_csv)
        saved = self.save_the_filtered_csv(y_lables)
        return saved


# c = CombinedCsv()
# y=c.clean_csv(c)
# print(y.info())
