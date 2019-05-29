import dataset
import betting
import tensorflow as tf
import numpy as np
import csv
import main

TRAINING_SET_SPLIT = 0.90

class Model:
    def begin(self, edge, strategy):
        data = dataset.Dataset('data/data.csv')

        self.train_results_len = int(TRAINING_SET_SPLIT * len(data.processed_results))
        self.train_results = data.processed_results[:self.train_results_len]
        self.test_results = data.processed_results[self.train_results_len:]
        self.test_results_info = [[]for i in range(7)]
        for i in range(3):
            self.test_results_info[i] = data.result_info[i][self.train_results_len:]

        def map_results(results):
            features = {}

            for result in results:
                for key in result.keys():
                    if key not in features:
                        features[key] = []

                    features[key].append(result[key])

            for key in features.keys():
                features[key] = np.array(features[key])
            return features, features['result']

        self.train_features, self.train_labels = map_results(self.train_results)
        self.test_features, self.test_labels = map_results(self.test_results)

        return self.learn(edge, strategy)


    def learn(self, edge, strategy):
        self.display = []

        with open('Model.csv', 'w', newline='') as stream:
            writer = csv.writer(stream)
            self.get_model().train(input_fn=self.train_input_fn(), steps=100)
            evaluation_result = self.get_model().evaluate(input_fn=self.test_input_fn())
            predictions = list(self.get_model().predict(input_fn=self.test_input_fn()))
            for pred in predictions:
                self.test_results_info[3].append(round(pred['probabilities'][0], 2))
                self.test_results_info[4].append(round(pred['probabilities'][1], 2))
                self.test_results_info[5].append(round(pred['probabilities'][2], 2))
                self.test_results_info[6].append(str(pred['classes']))
            prediction_result = betting.test_betting_stategy(predictions, self.test_features,
                                                             self.test_labels, self.test_results_info, edge, strategy)

            writer.writerow([evaluation_result['accuracy'], evaluation_result['average_loss'], prediction_result['performance']])
            self.display.append(prediction_result)
            self.display.append(evaluation_result)
            with open('Predictions.csv', 'w', newline='') as out:
                writer = csv.writer(out)
                writer.writerow(["Home", "Away", "Date", "P(H)", "P(D)", "P(A)", "P"])
                for j in range(len(self.test_results_info[0])):
                    writer.writerow([self.test_results_info[0][j], self.test_results_info[1][j], self.test_results_info[2][j].strftime('%d-%m-%Y'),
                                     self.test_results_info[3][j], self.test_results_info[4][j], self.test_results_info[5][j], self.test_results_info[6][j].replace("b", "").replace("['", "").replace("']", "")])
        return self.display

    def test_input_fn(self):
        return tf.estimator.inputs.numpy_input_fn(
            x=self.test_features,
            y=self.test_labels,
            num_epochs=1,
            shuffle=False
        )

    def train_input_fn(self):
        return tf.estimator.inputs.numpy_input_fn(
            x=self.train_features,
            y=self.train_labels,
            batch_size=500,
            num_epochs=None,
            shuffle=True
        )

    def get_feature_columns(self):
        feature_columns = []
        for mode in ['home', 'away']:
            feature_columns = feature_columns + [
                tf.feature_column.numeric_column(key='{}-wins'.format(mode)),
                tf.feature_column.numeric_column(key='{}-draws'.format(mode)),
                tf.feature_column.numeric_column(key='{}-losses'.format(mode)),
                tf.feature_column.numeric_column(key='{}-goals'.format(mode)),
                tf.feature_column.numeric_column(key='{}-opposition-goals'.format(mode)),
                tf.feature_column.numeric_column(key='{}-shots'.format(mode)),
                tf.feature_column.numeric_column(key='{}-shots-on-target'.format(mode)),
                tf.feature_column.numeric_column(key='{}-opposition-shots'.format(mode)),
                tf.feature_column.numeric_column(key='{}-opposition-shots-on-target'.format(mode)),
            ]
        return feature_columns

    def get_model(self):
        model = tf.estimator.DNNClassifier(
            model_dir='model/',
            hidden_units=[10],
            feature_columns=self.get_feature_columns(),
            n_classes=3,
            label_vocabulary=['H', 'D', 'A'],
            optimizer=tf.train.ProximalAdagradOptimizer(
                learning_rate=0.08,
                l1_regularization_strength=0.001
            ))
        return model

if __name__ == '__main__':
    main.main()


