import pickle
from google.cloud import storage
from config import MODEL_PATH
from sklearn.preprocessing import StandardScaler #

m = [ 0.3864818 ,  0.6135182 , 47.48526863, 41.6440208 , 68.2254766 ,
       26.66724437, 33.86533795, 10.72443674,  8.21559792,  5.38807626,
       81.80034662, 38.48110919, 71.92097054] #
s = [ 0.48694314,  0.48694314,  9.9339347 ,  5.76306321, 25.92843088,
       20.90898702, 33.11722697, 15.50703454,  2.18154868,  1.128455  ,
       51.13448778, 54.72249203,  5.36894534] #

def hepatitis_predict(request):
    req_json = request.get_json()
    if req_json:
        storage_client = storage.Client()

        bucket = storage_client.bucket(MODEL_PATH.replace('gs://', '').split('/')[0])
        blob = bucket.blob("/".join(MODEL_PATH.replace('gs://', '').split('/')[1:]))
        pickle_in = blob.download_as_string()
        ml_model = pickle.loads(pickle_in)

        try:
            sc = StandardScaler() #
            sc.mean_ = m #
            sc.scale_= s #
            k = sc.transform([req_json['value']]) #
            Ypredict = ml_model.predict(k) #
            dic_map = {0: "Blood Donor", 1: "Hepatitis", 2: "Fibrosis", 3: "Cirrhosis"}
            return {'result': dic_map[int(Ypredict[0])]} #
        
        except Exception as e:
            return e
    else:
        return 'hello World'
