from CombinedCsv import CombinedCsv
from Dataset import Dataset
from PreprocessData import PreprocessData
from SaveModel import SaveModel
import tensorflow as tf
import numpy as np
import itertools




def main():
    combine_csv = CombinedCsv()
    combine_csv.clean_csv(combine_csv)
    p = PreprocessData()
    p.make_csv_sound_type()
    sounds = ['s_cough', 'h_cough', 's_breath', 'F_count', 'vowel_E', 'vowel_O']
    for s in sounds:
        d = Dataset(s)
        d.samples()
        m = SaveModel(s, 'sounds_dataset')
        split_dataset = m.LoadData()
        m.ModelEvaluation(split_dataset)
        # p = predictmodel(m)

    # example function to average the results from each sound type model
    def predictmodel(m):

        print(m.soundType)
        print('*****************************************************************************************************')
        model = tf.keras.models.load_model('models/{}_model'.format(m.soundType))
        # p_pred = model.predict(m.xtest[:10])
        # y_pred = np.where(p_pred > 0.5, 1, 0)
        #
        # res = list(itertools.chain(*p_pred))
        # print(",".join(map(str, res)))
        # print('predicted:',y_pred.flatten())
        res = list(itertools.chain(*m.y_test[:20]))
        print("real:", res)
        if 1 in res:
            print("yes")
            pos = res.index(1)
            print("index:", str(pos))
            pos_y = m.y_test[:20][pos]
            print("array_index_value:", str(pos_y))
            pos_x = m.xtest[:20][pos_y]
            p_pred = model.predict(pos_x)
            y_pred = np.where(p_pred > 0.5, 1, 0)
            print("prob:", str(p_pred))
            print('real:', str(pos_y))
            print('predicted:', str(y_pred))

        print('*****************************************************************************************************')


if __name__ == "__main__":
    main()
