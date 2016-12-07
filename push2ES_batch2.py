# 2. Push data into ElasticSearch

# What do I need?
import json
import pyes # Package to dump YouTube data to ElasticSearch (https://pyes.readthedocs.io/en/latest/references/pyes.es.html)
import sys
from retrieveData_batch import retrieveAPIData
reload(sys)
sys.setdefaultencoding('utf-8') # For displaying foreign characters

class push2ES:

    def __init__(self, index):
        self.apiCall = retrieveAPIData.main(index)
        self.tFrame = self.apiCall.tFrame

    def pushToES(self):

        ttComplete = self.tFrame

        # Add a id for looping into ElasticSearch index
        ttComplete["no_index"] = range(1,len(ttComplete)+1)

        # Convert DataFrame into json
        tmp = ttComplete.reset_index().to_json(orient="records")

        # Load each record into jon format before bulk
        tmp_json = json.loads(tmp)
        #print("Convert Dataframe into Json view:")
        #print("total number of json list is:")
        #print(len(tmp_json))
        #print(tmp_json[1:3])

        index_name = 'youtube'
        type_name = 'pyelastic'
        es = pyes.ES()

        i = 1
        for doc in tmp_json:
            print "Document in tmp_json: " + str(i)
            try:
              es.index(doc, index_name, type_name)
            except:
              e = sys.exc_info()[0]
              print e
              pass
            i=i+1

        #print("Number of doc in the batch")
        #print(i-1)

#pushCall = push2ES()
#pushCall.pushToES()

i=1

while i < 4801:
    print("Current Document: " + str(i))
    pushCall = push2ES(i)
    pushCall.pushToES()
    i=i+1
else:
    print("Done")