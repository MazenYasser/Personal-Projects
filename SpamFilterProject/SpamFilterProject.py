# Spam Filter
# Steps: 
# 1- Read csv file, 2- Pre processing, 3- Feature extraction, 4- Rearrange the file in proper format
# Step 2: Remove Stopwords,Special chars,lower all case,Stem the words
# Step 3: Define unique words in mails to use it as feature (Words in spam vs ham)

import csv
import pandas as pd
import numpy as np
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


dataset= pd.read_csv('spam.csv', encoding='latin-1')

# Splitting the file into 2 columns, one for mail and one for Category(Spam vs ham)
mails=pd.DataFrame(dataset.iloc[:,1])
mail_category=pd.DataFrame(dataset.iloc[:,0])

# Defining required methods
stemmer=PorterStemmer()
def stem_words(sentence):
    return ' '.join([stemmer.stem(word) for word in sentence.split()])

filtered_words=[]
# i am studying physics and i am studying data
def vectorize(tokens):
    vector=[]

    for word in filtered_words:
        vector.append(tokens.count(word))
    
    return vector

def unique_words(sentence):
    seen= set()
    return [word for word in sentence if not (word in seen or seen.add(word))]

STOPWORDS= set(stopwords.words('english'))
def remove_stopwords(text):
    return ' '.join([word for word in str(text).split() if word not in STOPWORDS])

special_chars= string.punctuation
def remove_specials(sentence):
        return sentence.translate(str.maketrans('','',special_chars))

# Defining required containers
filtered_words=[]

spam_dict={}
ham_dict={}

ham_list=[]
spam_list=[]

ham_vector=[]
spam_vector=[]

# Making a list of spam mails and a list of ham mails
with open('spam.csv', 'r', encoding='latin-1') as file:
    myCsv= csv.reader(file)
    rows= list(myCsv)
    row_num=0
    for row in rows:
        if rows[row_num][0] == 'spam':
            spam_list.append(rows[row_num][1])

        elif rows[row_num][0] == 'ham':
            ham_list.append(rows[row_num][1])
        row_num+=1

# Pre processing mails
for mail in mails.Mail:

    spam_check=False
    if mail in spam_list:
        spam_check=True
    elif mail in ham_list:
        spam_check=False
    
    mail= mail.lower()
    mail= remove_specials(mail)
    mail= stem_words(mail)
    mail= remove_stopwords(mail)
    
    tokens= mail.split()
    vocab= unique_words(tokens)
    
    # Creating a list of unique words 
    for word in vocab:
        if word not in filtered_words:
            filtered_words.append(word)
    
    # Creating a dictionary of spam words, making sure that mail is spam before adding the word to the dictionary
    if spam_check == True:
        spam_vector.extend(vectorize(tokens))
        if len(spam_dict)!=0:
            for word in vocab:
                if word in spam_dict:
                    spam_dict.update({word : spam_dict[word]+1})
                else:
                    spam_dict.update({word : 1})
        else:
            spam_dict=dict(zip(filtered_words, spam_vector))
    
    # Creating a dictionary of ham words, making sure that mail is ham before adding the word to the dictionary
    else:
        ham_vector.extend(vectorize(tokens))
        
        if len(ham_dict)!=0:
            for word in vocab:
                if word in ham_dict:
                    ham_dict.update({word : ham_dict[word]+1})
                else:
                    ham_dict.update({word : 1})
        else:
            ham_dict=dict(zip(filtered_words, ham_vector))

# Feature extraction
# Sorting the dictionaries by Value in descending order
spam_dict= sorted(spam_dict.items(), key= lambda mail:mail[1], reverse=True)
ham_dict= sorted(ham_dict.items(), key= lambda mail:mail[1], reverse=True)

# Getting the 30% training samples from the dictionaries
ham_training_count= int((len(ham_dict)*30)/100)
ham_training_sample= ham_dict[:ham_training_count]
spam_training_count= int((len(spam_dict)*30)/100)
spam_training_sample= spam_dict[:spam_training_count]

# This training sample contains the final list of words (Features) to be included in the csv file
training_sample= ham_training_sample + spam_training_sample

# Writing data to a csv file
with open("FinalSample.csv", 'w+', newline='') as file:
    writer=csv.writer(file)

# This list content is the same as training_sample, but arranged in a different format to avoid file writing problems
    rows_list= [[first_word[0] for first_word in training_sample]]

# Adding the Output column at the end to show spam or ham
    rows_list[0].append('Output')
    writer.writerows(rows_list)

# This list contains the values of the first column in the dataset (spam vs ham)
    category_list=mail_category['Output']
    category_count=0
    vector=[]
# Processing words data before writing them to the vectors
    for mail in mails.Mail:
       
        mail= mail.lower()
        mail= remove_specials(mail)
        mail= stem_words(mail)
        mail= remove_stopwords(mail)
        tokens= mail.split()
        
        for word in rows_list[0]:
            vector.append(tokens.count(word))
    # Since we added Output column in the end, it will put zeros for all column values since Output doesn't exist in mails
    # So we pop the last values of the vector to replace it with spam/ham values
        vector.pop()
        vector.append(category_list[category_count])
        writer.writerow(vector)
    
    # Clearing vector to avoid added values and incrementing the Output column count
        vector.clear()
        category_count+=1

# Trainning model using Logistic Regression and KNN then displaying final results of each method
print('Using Logistic Regression')
print('--------------------------')
dataset = pd.read_csv('FinalSample.csv')

x = pd.DataFrame(dataset.iloc[:,:-1])
y = pd.DataFrame(dataset.iloc[:,-1])

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=1)

from sklearn.linear_model import LogisticRegression
reg_model = LogisticRegression()
reg_model.fit(x_train, np.ravel(y_train)) 
y_predict = reg_model.predict(x_test)

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_predict)
print(confusion_matrix)

from sklearn.metrics import classification_report
print(classification_report(y_test, y_predict))

print('-------------------------------------')
print('Using KNN')
print('------------')

x_train,x_test,y_train,y_test=train_test_split(x,y, test_size=0.2, random_state=1)

from sklearn.neighbors import KNeighborsClassifier
knn_model=KNeighborsClassifier(n_neighbors=1)
knn_model.fit(x_train, np.ravel(y_train))
y_predict=knn_model.predict(x_test)

from sklearn.metrics import confusion_matrix
confusion_matrix=confusion_matrix(y_test,y_predict)
print(confusion_matrix)

print(classification_report(y_test,y_predict))