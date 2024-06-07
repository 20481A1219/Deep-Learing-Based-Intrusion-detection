from keras.models import load_model
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
from tensorflow.keras.utils import to_categorical
import twilio.rest
import smtplib

model = load_model('/home/batch-a6/Documents/CNN_WLSTM-99.99.h5')

# Load and preprocess the new data
data = pd.read_excel("/home/batch-a6/Documents/test_data.xlsx", header=None)

def data_spli_to_fit(data):
    data = data.drop([0],axis=1)
    data = data.drop([1],axis=1)
    data = data.drop([2],axis=1)
    data = data.drop([3],axis=1)
    data[47] = data[47].fillna('Normal')
    data[47] = data[47].replace(' Fuzzers','Fuzzers')
    data[47] = data[47].replace(' Fuzzers ','Fuzzers')
    data[47] = data[47].replace(' Reconnaissance','Reconnaissance')
    data[47] = data[47].replace(' Reconnaissance ','Reconnaissance')
    data[47] = data[47].replace(' Shellcode','Shellcode')
    data[47] = data[47].replace(' Shellcode ','Shellcode')
    data[47] = data[47].replace('Backdoors','Backdoor')
    data = data.fillna(0)
    data[39] = data[39].replace(' ',0)
    data[39] = data[39].astype('int64')
    data_2_type = data[4].unique().tolist() 
    data_3_type = data[5].unique().tolist() 
    data_4_type = data[13].unique().tolist() 
    data = data.drop([48], axis=1) #删除Label
    data[4]= data[4].apply(lambda x : data_2_type.index(x))
    data[5] = data[5].apply(lambda x : data_3_type.index(x))
    data[13] = data[13].apply(lambda x : data_4_type.index(x))
    unlabled_data = data.drop([47],axis=1)
    return(unlabled_data, pd.DataFrame(data[47]))

def data_s(data):
    data_43_type = ['Normal', 'Exploits', 'Reconnaissance', 'DoS', 'Generic', 'Shellcode', 'Fuzzers', 'Worms', 'Backdoor', 'Analysis']
    data[47] = data[47].apply(lambda x : data_43_type.index(x))
    res = to_categorical(data[47], num_classes=10)
    return (data, res)

(data,res) =  data_spli_to_fit(data)
scaler = MinMaxScaler(feature_range=(0,1))
scaler.fit(data)
data = pd.DataFrame(scaler.transform(data))
data = pd.concat([data, res],axis=1)
(data,res) = data_s(data)

# Perform inference using the pre-trained model
predictions = model.predict(data, batch_size=2048)
predicted_classes = np.argmax(predictions, axis=1)
print(predicted_classes)
normal=list(predicted_classes)s.count(0)
attacks=len(predicted_classes)-normal 
if attacks>=1 and normal>=1:
	print("Sending Mail")
	HOST = "smtp-mail.outlook.com"
	PORT = 587

	FROM_EMAIL = "hruday.boppa@outlook.com"
	TO_EMAIL = "hruday.boppa@gmail.com"
	PASSWORD = "Hruday<me>me19"

	MESSAGE = """Subject: Intrusion Detection!!!

	Someone intruded through your raspberry pi network. Hurry up!
	"""

	smtp = smtplib.SMTP(HOST, PORT)

	status_code, response = smtp.ehlo()
	print(f"[*] Echoing the server: {status_code} {response}")

	status_code, response = smtp.starttls()
	print(f"[*] Starting TLS connection: {status_code} {response}")

	status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
	print(f"[*] Logging in: {status_code} {response}")

	smtp.sendmail(FROM_EMAIL, TO_EMAIL, MESSAGE)
	smtp.quit()
	print("Mail Sent")
	print("Sending Message")
	client = twilio.rest.Client("ACf23bb0e70ce0993029fd32f642ba2383", "2d4131c30869fbefeefd0bca5bb2b960")
	from_ = "+12056866292"
	to = "+918143266869"
	message = "Your RaspberryPi is found in intrusion."
	message = client.messages.create(
		to=to,
		from_=from_,
		body=message
	)
	print(message.sid)
	print("Message Sent")
else:
	print("No attacks found")

	
