import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch import optim
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
import json
import random
import neattext as nt
import spacy






dataFile = '_ralph_memory.json'


def Train_Model(data_file):
    def tokenize(sentence):
        return nltk.word_tokenize(sentence)

    stemmer = PorterStemmer()
    def stem(word):
        return stemmer.stem(word.lower())

    def bag_of_words(tokenized_sentenced, all_words):
        tokenized_sentenced = [stem(w) for w in tokenized_sentenced]
        bag = np.zeros(len(all_words), dtype=np.float32)
        for idx, word in enumerate(all_words):
            if word in tokenized_sentenced:
                bag[idx] = 1.0

        return bag



    with open(data_file, 'r') as f:
        data = json.load(f)

    all_words = []
    tags = []
    xy = []

    for intend in data['memory']:
        tag = intend['tag']
        tags.append(tag)

        for pattern in intend['patterns']:
            word = tokenize(pattern)
            all_words.extend(word)
            xy.append((word, tag))

    ignore = ['?', '!', '.', ',']

    all_words = [stem(w) for w in all_words if w not in ignore]
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))

    X_train = []
    y_train = []
    for (pattern_sentence, tag) in xy:
        bag = bag_of_words(pattern_sentence, all_words)
        X_train.append(bag)

        label = tags.index(tag)
        y_train.append(label)

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    #creating dataset
    class ChatDataset(nn.Module):
        def __init__(self):
            self.number_of_samples = len(X_train)
            self.X_train = X_train
            self.y_train = y_train

        def __getitem__(self, idx):
            return self.X_train[idx], self.y_train[idx]

        def __len__(self):
            return self.number_of_samples


    dataset = ChatDataset()
    train_loader = DataLoader(dataset=dataset, batch_size=8, shuffle=True)


    #creating the model
    class ChatBotModel(nn.Module):
        def __init__(self, input_size, hidden_size, output_size):
            super(ChatBotModel, self).__init__()

            self.layer1 = nn.Linear(input_size, hidden_size)
            self.layer2 = nn.Linear(hidden_size, hidden_size)
            self.output = nn.Linear(hidden_size, output_size)
            self.relu = nn.ReLU()

        def forward(self, x):
            x = self.layer1(x)
            x = self.relu(x)
            x = self.layer2(x)
            x = self.relu(x)
            x = self.output(x)

            return x


    input_size = len(X_train[0])
    hidden_size = 8
    output_size = len(tags)

    model = ChatBotModel(input_size, hidden_size, output_size)

    #training
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    epochs = 1000

    for epoch in range(epochs):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = (torch.tensor(labels, dtype= torch.long)).to(device)

            #forward pass
            output = model(words)
            #loss
            loss = criterion(output, labels)
            #backward pass
            optimizer.zero_grad()
            loss.backward()
            #optimization
            optimizer.step()

        if ((epoch+1) % 100)==0:
            print(f'epoch: {epoch+1}/{epochs}, loss: {loss.item():.4f}')
    print(f'\n Accuracy: {(100-(loss.item()*100)):.2f}%')
    print("Model has been trained")

    #saving the model and its data
    data = {
     "model_state": model.state_dict(),
     "input_size": input_size,
     "hidden_size": hidden_size,
     "output_size": output_size,
     "all_words": all_words,
     "tags": tags
    }

    modelDataFile = "_Chat.pth"
    torch.save(data, modelDataFile)
    print("Your model has been saved as _Chat.pth")






#Train_Model(dataFile)






def Converse(sentence, mem):
    def tokenize(sentence):
        return nltk.word_tokenize(sentence)

    stemmer = PorterStemmer()
    def stem(word):
        return stemmer.stem(word.lower())

    def bag_of_words(tokenized_sentenced, all_words):
        tokenized_sentenced = [stem(w) for w in tokenized_sentenced]
        bag = np.zeros(len(all_words), dtype=np.float32)
        for idx, word in enumerate(all_words):
            if word in tokenized_sentenced:
                bag[idx] = 1.0

        return bag


    def get_message_subject(sentence):
        global subject
        global name
        global other_noun
        p_sentence = list(([sentence])[0].split())
        sentx = nt.TextFrame(text=str(sentence))
        s = sentx.remove_stopwords()
        check =  ([s.text])[0].split()
        n = ''
        for i in check:
            n += i + " "
        new_string = n[:-1]
        nlp = spacy.load("en_core_web_sm")
        ppnouns = []
        check2 = ['play', 'run', 'joke', 'story', 'color', 'sing', 'eat', 'drink', 'kick', 'wife', 'new', 'husband', 'launch', 'breakfast', 'supper', 'dinner', 'meal']
        for word in nlp(new_string):
            if word.pos_ == 'PROPN':
                if word.text not in check2:
                    ppnouns.append(word.text)
        nameList = list(set(ppnouns))
        if len(nameList)>0:
            n2 = ''
            for i in nameList:
                n2 += i + " "
            nme = n2[:-1]
            if nme!='ralph':
                subject = nme
            else:
                subject = 'None'
        else:
            subject = 'None'
        # text = nltk.word_tokenize(sentence)
        # pos_tagged = nltk.pos_tag(text)
        # nouns = filter(lambda x:x[1]=='NN',pos_tagged)
        # nounList = []
        # for i in nouns:
        #     nounList.append(i[0])
        # if len(nounList)>0:
        #     check4 = ['morning', 'afternoon', 'evening', 'night']
        #     for i in nounList:
        #         if i!=name and i not in check4:
        #             other_noun = i
        #         else:
        #             other_noun = 'None'
        # else:
        #     other_noun = 'None'
        # print(f'name: {name}')
        # print(f'other_noun: {other_noun}')
        # if name!='None' and other_noun!='None':
        #     if name in p_sentence and other_noun in p_sentence:
        #         if p_sentence.index(name)<p_sentence.index(other_noun):
        #             subject = name
        #         elif p_sentence.index(other_noun)>p_sentence.index(name):
        #             subject = other_noun
        #     else:
        #         subject = name
        # elif name!='None' and other_noun=='None':
        #     subject = name
        # elif name=='None' and other_noun!='None':
        #     subject = other_noun
        # else:
        #     subject = 'None'


        return subject



    class ChatBotModel(nn.Module):
        def __init__(self, input_size, hidden_size, output_size):
            super(ChatBotModel, self).__init__()
            self.layer1 = nn.Linear(input_size, hidden_size)
            self.layer2 = nn.Linear(hidden_size, hidden_size)
            self.output = nn.Linear(hidden_size, output_size)
            self.relu = nn.ReLU()
        def forward(self, x):
            x = self.layer1(x)
            x = self.relu(x)
            x = self.layer2(x)
            x = self.relu(x)
            x = self.output(x)
            return x


    with open(dataFile, 'r') as f:
        memories = json.load(f)
    model_data = torch.load('_Chat.pth')
    input_size = model_data['input_size']
    hidden_size = model_data['hidden_size']
    output_size = model_data['output_size']
    all_words = model_data['all_words']
    tags = model_data['tags']
    model_state = model_data['model_state']
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = ChatBotModel(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    global sentence2
    if ('ralph' in sentence and sentence!='ralph'):
        stce = list((([sentence])[0].split()))
        stce.remove('ralph')
        temp = ''
        for i in stce:
            temp += i + ' '
            sentence2 = temp[:-1]
    else:
        sentence2 = sentence


    sentence = tokenize(sentence2)
    #print(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    response_probabilities = torch.softmax(output, dim=1)
    possible_response_probability = response_probabilities[0][predicted.item()]
    #print(f'probability: {possible_response_probability.item():.2f}')


    global response

    if (("my" in sentence and "name" in sentence) and "what" not in sentence):
        response = "Nice to meet you"
    else:
        if possible_response_probability.item() >= 0.8:
            for memory in memories['memory']:
                if tag == memory['tag']:
                    responses = memory['responses']
                    response = random.choice(responses)
                    #handle some commands here, based on response
        else:
            response = None


    return response








#print(Converse('i need your help please', {'first thing': 1, 'second thing': 2, 'last thing': 3}))
