import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, hamming_loss
from sklearn.feature_extraction.text import TfidfVectorizer
import neattext as nt
import neattext.functions as nt_fx
from skmultilearn.problem_transform import LabelPowerset
import pickle






dataFile = '_ralph_memory.csv'


def Train_Model(data_file):

    #loading the data
    df = pd.read_csv(data_file)

    #Text Preprocessing:
    #exploring the sentence column data for noise
    df['sentence'].apply(lambda x: nt.TextFrame(x).noise_scan())
    #extracting the stopwords
    df['sentence'].apply(lambda x: nt.TextExtractor(x).extract_stopwords())
    #removing the stopwords
    sentences = df['sentence'].apply(nt_fx.remove_stopwords)

    #Feature engineering
    tfidf = TfidfVectorizer()
    Xfeatures = tfidf.fit_transform(sentences).toarray()
    with open("_intend_vectorizer", "wb") as vectorizer:
        pickle.dump(tfidf, vectorizer)
    yfeatures = df[list(df.columns[1:])]

    #Model building:
    #splitting the data
    X_train, X_test, y_train, y_test = train_test_split(Xfeatures, yfeatures, test_size=0.3, random_state=42)
    #converting multilabel problem to multiclass problem: Binary classification
    Intend_Model = LabelPowerset(MultinomialNB())

    #training the model
    Intend_Model.fit(X_train, y_train)

    #Testing the model
    test_prediction = Intend_Model.predict(X_test).toarray()

    #accuracy of the model
    correct = accuracy_score(y_test, test_prediction)*100
    print('Percentage Correct: {:.2f}%'.format(correct))
    incorrect = hamming_loss(y_test, test_prediction)*100
    print('Percentage Incorrect: {:.2f}%'.format(incorrect))


    #saving the trained model
    with open("_Intend_Extractor", "wb") as model:
        pickle.dump(Intend_Model, model)





#Train_Model(dataFile)




def Extract_Intend(sentence):

    global intend
    global intend_target

    df = pd.read_csv(dataFile)

    processed_message = ([sentence])[0].split()

    #loading the model vectorizer
    with open('_intend_vectorizer', "rb") as vectorizer:
        tfidf = pickle.load(vectorizer)
    #loading the trained model
    with open('_Intend_Extractor', "rb") as model:
        Intend_Model = pickle.load(model)
    #doing the prediction and retrieving the message intend
    prepared_sentence = tfidf.transform([sentence])
    prediction = Intend_Model.predict(prepared_sentence).toarray()
    #print(prediction)
    temp = []
    keywords = set(df['sentence'])
    intends = list(df.columns[1:])
    for dimension in prediction:
        for value in dimension:
            temp.append(value)
    sentx = nt.TextFrame(text=sentence)
    s = sentx.remove_stopwords()
    check =  ([s.text])[0].split()
    #print(check)

    try:
        if 'show' in processed_message and ('picture' in processed_message or 'photo' in processed_message or 'image' in processed_message):
            intend = 'show picture'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('on' in processed_message) and ('wifi' in processed_message):
            intend = 'connect wifi'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('off' in processed_message) and ('wifi' in processed_message):
            intend = 'disconnect wifi'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('on' in processed_message) and ('music' in processed_message or 'song' in processed_message or 'audio' in processed_message):
            intend = 'play audio'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('off' in processed_message) and ('music' in processed_message or 'song' in processed_message or 'audio' in processed_message):
            intend = 'stop audio'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('on' in processed_message) and ('movie' in processed_message or 'film' in processed_message or 'video' in processed_message):
            intend = 'play video'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('off' in processed_message) and ('movie' in processed_message or 'film' in processed_message or 'video' in processed_message):
            intend = 'stop video'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('on' in processed_message) and (('virtual' in processed_message and 'mouse' in processed_message) or 'vm' in processed_message or ('v' in processed_message and 'm' in processed_message)):
            intend = 'activate vm'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('off' in processed_message) and (('virtual' in processed_message and 'mouse' in processed_message) or 'vm' in processed_message or ('v' in processed_message and 'm' in processed_message)):
            intend = 'deactivate vm'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('on' in processed_message) and (('gesture' in processed_message and 'volume' in processed_message) or 'gv' in processed_message or 'gvc' in processed_message or ('g' in processed_message and 'v' in processed_message)):
            intend = 'activate gvc'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('off' in processed_message) and (('gesture' in processed_message and 'volume' in processed_message) or 'gv' in processed_message or 'gvc' in processed_message or ('g' in processed_message and 'v' in processed_message)):
            intend = 'deactivate gvc'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('on' in processed_message) and (('gesture' in processed_message and 'brightness' in processed_message) or 'gb' in processed_message or 'gbc' in processed_message or ('g' in processed_message and 'b' in processed_message)):
            intend = 'activate gbc'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('off' in processed_message) and (('gesture' in processed_message and 'brightness' in processed_message) or 'gb' in processed_message or 'gbc' in processed_message or ('g' in processed_message and 'b' in processed_message)):
            intend = 'deactivate gbc'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('on' in processed_message) and ('computer' in processed_message or 'machine' in processed_message or 'pc' in processed_message or 'laptop' in processed_message):
            intend = 'turn-on pc'
        elif ('turn' in processed_message or 'put' in processed_message or 'switch' in processed_message) and ('off' in processed_message) and ('computer' in processed_message or 'machine' in processed_message or 'pc' in processed_message or 'laptop' in processed_message):
            intend = 'shutdown pc'
        elif 'up' in processed_message and 'scroll' not in processed_message and 'page' not in processed_message and 'play' not in processed_message and 'open' not in processed_message:
            intend = 'up'
        elif 'down' in processed_message and 'scroll' not in processed_message and 'page' not in processed_message and 'play' not in processed_message and 'open' not in processed_message:
            intend = 'down'
        elif 'right' in processed_message and 'click' not in processed_message and 'play' not in processed_message and 'open' not in processed_message:
            intend = 'right'
        elif 'left' in processed_message and 'click' not in processed_message and 'play' not in processed_message and 'open' not in processed_message:
            intend = 'left'
        elif 'scroll' in processed_message and 'up' in processed_message and 'play' not in processed_message and 'open' not in processed_message:
            if processed_message.index('scroll')<processed_message.index('up') or processed_message.index('scroll')>processed_message.index('up'):
                    if processed_message.index('scroll')==processed_message.index('up')-1 or processed_message.index('scroll')==processed_message.index('up')+1:
                        intend = 'scroll up'
        elif 'scroll' in processed_message and 'down' in processed_message and 'play' not in processed_message and 'open' not in processed_message:
            if processed_message.index('scroll')<processed_message.index('down') or processed_message.index('scroll')>processed_message.index('down'):
                    if processed_message.index('scroll')==processed_message.index('down')-1 or processed_message.index('scroll')==processed_message.index('down')+1:
                        intend = 'scroll down'
        elif 'page' in processed_message and 'up' in processed_message and 'play' not in processed_message and 'open' not in processed_message:
            if processed_message.index('page')<processed_message.index('up') and processed_message.index('page')==processed_message.index('up')-1:
                intend = 'page up'
        elif 'page' in processed_message and 'down' in processed_message and 'play' not in processed_message and 'open' not in processed_message:
            if processed_message.index('page')<processed_message.index('down') and processed_message.index('page')==processed_message.index('down')-1:
                intend = 'page down'
        elif 'click' in processed_message and 'right' not in processed_message:
            intend = 'click' #select
        elif 'left' in processed_message and 'click' in processed_message:
            if processed_message.index('left')<processed_message.index('click') and processed_message.index('left')==processed_message.index('click')-1:
                intend = 'left click' #select
        elif 'left-click' in processed_message:
            intend = 'left click'
        elif 'right' in processed_message and 'click' in processed_message:
            if processed_message.index('right')<processed_message.index('click') and processed_message.index('right')==processed_message.index('click')-1:
                intend = 'right click'
        elif 'right-click' in processed_message:
            intend = 'right click'
        elif 'back' in processed_message:
            intend = 'backward'
        elif 'front' in processed_message:
            intend = 'forward'
        elif 'select' in processed_message and 'all' in processed_message:
            if processed_message.index('select')<processed_message.index('all') and processed_message.index('select')==processed_message.index('all')-1:
                intend = 'select all' #ctrl a
        # elif 'open' in processed_message and len(processed_message)==1:
        #     intend = 'click'
        elif ('command' in processed_message and 'prompt' in processed_message) or 'commandprompt' in processed_message or 'prompt' in processed_message or 'commandline' in processed_message or ('command' in processed_message and 'line' in processed_message) or 'cmd' in processed_message or ('c' in processed_message and 'm' in processed_message and 'd' in processed_message):
            intend = 'command prompt'
        elif ('power' in processed_message and 'shell' in processed_message) or 'powershell' in processed_message or 'shell' in processed_message:
            intend = 'powershell'
        elif (('press' in processed_message) and (len(processed_message[processed_message.index('press')+1])==1)):
            intend = 'press key'
            intend_target = processed_message[processed_message.index('press')+1]
            return intend, intend_target
        elif (('hold' in processed_message) and (len(processed_message[processed_message.index('hold')+1])==1)):
            intend = 'hold key'
            intend_target = processed_message[processed_message.index('hold')+1]
            return intend, intend_target
        elif 'repeat' in processed_message:
            intend = 'repeat'
            intend_target = None
            return intend, intend_target

        elif 'search' in processed_message:
            intend = 'search'
            if 'for' in processed_message:
                intend_target = ' '.join(processed_message[processed_message.index('for')+1:])
            else:
                intend_target = ' '.join(processed_message[processed_message.index('search')+1:])
            return intend, intend_target

        elif ('open' in processed_message and ('file' not in processed_message and 'folder' not in processed_message and 'folders' not in processed_message and 'program' not in processed_message and 'application' not in processed_message and 'app' not in processed_message) and 'project' not in processed_message and 'main' not in processed_message and 'favorite' not in processed_message and 'start' not in processed_message and 'settings' not in processed_message and 'center' not in processed_message and 'hidden' not in processed_message):
            intend = 'open'
            intend_target = None
            return intend, intend_target
        elif ('resume' in processed_message and ('audio' in processed_message or 'music' in processed_message or 'song' in processed_message)):
            intend = 'resume audio'
            intend_target = None
            return intend, intend_target
        elif ('pause' in processed_message and ('audio' in processed_message or 'music' in processed_message or 'song' in processed_message)):
            intend = 'pause audio'
            intend_target = None
            return intend, intend_target
        elif ('next' in processed_message and ('audio' in processed_message or 'music' in processed_message or 'song' in processed_message)):
            intend = 'next audio'
            intend_target = None
            return intend, intend_target
        elif ('previous' in processed_message and ('audio' in processed_message or 'music' in processed_message or 'song' in processed_message)):
            intend = 'previous audio'
            intend_target = None
            return intend, intend_target
        elif ('resume' in processed_message and ('video' in processed_message or 'movie' in processed_message or 'film' in processed_message)):
            intend = 'resume video'
            intend_target = None
            return intend, intend_target
        elif ('pause' in processed_message and ('video' in processed_message or 'movie' in processed_message or 'film' in processed_message)):
            intend = 'pause video'
            intend_target = None
            return intend, intend_target
        elif ('next' in processed_message and ('video' in processed_message or 'movie' in processed_message or 'film' in processed_message)):
            intend = 'next video'
            intend_target = None
            return intend, intend_target
        elif ('previous' in processed_message and ('video' in processed_message or 'movie' in processed_message or 'film' in processed_message)):
            intend = 'previous video'
            intend_target = None
            return intend, intend_target
        elif ('forward' in processed_message and ('video' in processed_message or 'movie' in processed_message or 'film' in processed_message)):
            intend = 'forward video'
            intend_target = None
            return intend, intend_target
        elif ('backward' in processed_message and ('video' in processed_message or 'movie' in processed_message or 'film' in processed_message)):
            intend = 'backward video'
            intend_target = None
            return intend, intend_target
        elif ('resume' in processed_message and (('vlc' in processed_message) or ('video' in processed_message and 'media' in processed_message and 'player' in processed_message))):
            intend = 'resume vlc'
            intend_target = None
            return intend, intend_target
        elif ('pause' in processed_message and (('vlc' in processed_message) or ('video' in processed_message and 'media' in processed_message and 'player' in processed_message))):
            intend = 'pause vlc'
            intend_target = None
            return intend, intend_target
        elif ('next' in processed_message and (('vlc' in processed_message) or ('video' in processed_message and 'media' in processed_message and 'player' in processed_message))):
            intend = 'next vlc'
            intend_target = None
            return intend, intend_target
        elif ('previous' in processed_message and (('vlc' in processed_message) or ('video' in processed_message and 'media' in processed_message and 'player' in processed_message))):
            intend = 'previous vlc'
            intend_target = None
            return intend, intend_target



        else:
            check2 = []
            for i in keywords:
                sentx = nt.TextFrame(text=i)
                check2.append(([sentx.text])[0].split())
            #print(check2)
            possible_intend_keywords = []
            for possible_intend in intends:
                if temp[intends.index(possible_intend)] == 1:
                     for i in check2:
                         for j in i:
                            if (j in check or j in [s.text]):
                                #print(i)
                                possible_intend_keywords.append(i)
                     if len(possible_intend_keywords)>0:
                         intend = possible_intend
                     else:
                        intend = None

        #if intend_target==None:
        target = set()
        temp = set()
        temp2 = set()

        general_keyCommands = ['open', 'run', 'start', 'find', 'search', 'delete', 'remove', 'close', 'end', 'terminate', 'stop', 'end', 'play', 'stream', 'audio', 'music', 'song', 'video', 'movie', 'film', 'picture', 'application', 'app', 'program', 'website', 'browser', 'web browser', 'web page', 'file', 'folder', 'title', 'titled', 'called', 'named', 'weather']

        try:
            if intend!='stop audio' or intend!='stop video' or intend!='close picture':
                for i in general_keyCommands:
                    if i in check:
                        if i!=check[-1]:
                            temp.add(check[int(check.index(i))+1])
                for i in temp:
                    if i not in general_keyCommands:
                        target.add(i)
                for i in check:
                    if i not in target and i not in general_keyCommands:
                        if int(check.index(i)) == (int(check.index(list(target)[0])+1)):
                            temp2.add(i)
                            t = str(list(target)[0] + " " + list(temp2)[0])
                            target.remove(list(target)[0])
                            target.add(t)
                if len(target)>0:
                    intend_target = list(target)[0]
                else:
                    intend_target = None
            else:
                intend_target = None
        except:
            intend_target = None

    except:
        intend = None
        intend_target = None










    #returning required data
    try:
        return intend, intend_target
    except:
        return False













#print(Extract_Intend('update paths'))




