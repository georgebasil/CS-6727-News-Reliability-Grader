
from keras.layers import Dense
from keras.models import Sequential
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
import numpy
import pandas


def load_site_attributes(input_path):
	# Initialize the list of column names in the CSV file and then
	# Load it using Pandas
	cols = ["Domain", "Registrar", "Name", "Organization", "Country", "Private", "DomainAge", "DomainLifespan", "TimeUntilExpiration", "SinceLastUpdate", "NewsKeywords", "NewsInDomain", "DigitInDomain", "HyphenInDomain", "NameServerSLD", "NoveltyTLD", "DomainNameLength", "DomainResolves", "CertAvailable", "CertIssuer", "CertCountry", "CertLifeTime", "CertExpired", "SANCount", "SANWildCard", "SelfSignedCert", "WebsiteAS", "WebsiteCountry", "WebsiteCDN", "Score"]
	df = pandas.read_csv(input_path, sep=",", header=None, names=cols)
	return df


def process_site_attributes(df, train, test):
	# Initialize the column names of the continuous data
	continuous = ["DomainAge", "DomainLifespan", "TimeUntilExpiration", "SinceLastUpdate", "DomainNameLength", "CertLifeTime", "SANCount"]

	train_continuous = train[continuous]
	test_continuous = test[continuous]

	# One-hot encode the categorical data
	categorical = ["Registrar", "Name", "Organization", "Country", "Private", "NewsKeywords", "NewsInDomain", "DigitInDomain", "HyphenInDomain", "NameServerSLD", "NoveltyTLD", "DomainResolves", "CertAvailable", "CertIssuer", "CertCountry", "CertExpired", "SANWildCard", "SelfSignedCert", "WebsiteAS", "WebsiteCountry", "WebsiteCDN"]

	train_array = []
	test_array = []

	for key in categorical:
		binarizer = LabelBinarizer().fit(df[key].astype(str))
		train_categorical = binarizer.transform(train[key].astype(str))
		test_categorical = binarizer.transform(test[key].astype(str))

		train_array.append(train_categorical)
		test_array.append(test_categorical)

	train_array.append(train_continuous)
	test_array.append(test_continuous)

	# Construct the training and testing data points by concatenating the categorical features with the continuous ones
	train_x = numpy.hstack(train_array)
	test_x = numpy.hstack(test_array)

	# Return the concatenated training and testing data
	return train_x, test_x


# Load dataset
df = load_site_attributes('<PATH-TO-WORKING-DIRECTORY>\training_data.csv')

# Split dataset
(train, test) = train_test_split(df, test_size=0.50, random_state=42)

# Process dataset input
(trainX, testX) = process_site_attributes(df, train, test)

# Process dataset output
trainY = train["Score"]
testY = test["Score"]
hstack_testY = numpy.hstack(testY)

# Define the model
model = Sequential()
model.add(Dense(12, input_dim=trainX.shape[1], activation='relu', kernel_initializer='he_normal'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the keras model on the dataset
model.fit(trainX, trainY, epochs=200, batch_size=10)

# Evaluate the keras model
_, accuracy = model.evaluate(testX, testY)
print('Accuracy: %.2f' % (accuracy*100))

# Save model
model.save("<PATH-TO-WORKING-DIRECTORY>\saved_model_data")

exit(0)
