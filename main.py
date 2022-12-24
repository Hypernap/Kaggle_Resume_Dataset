import PyPDF2
import kaggle
import os
import abc

# QUESTION 1
dataset_name = 'snehaanbhawal/resume-dataset'
# Set the Kaggle API key and dataset name
kaggle.api.authenticate() # this authenticate using the API json downloaded from kaggle and stored at file {C:\Users\hp}\.kaggle

# Use the kaggle module to download the dataset
kaggle.api.dataset_download_files(dataset_name, unzip=True)

#to get the current working directoryu
root_dir=os.getcwd()

# A dictionary for all resume to get the options 
resume_all={}

#to get the data folder where all resumes are stored 
data_dir=os.path.join(root_dir,"data\data")

for i in os.listdir(data_dir):
    resume_all[i]=os.listdir(os.path.join(data_dir,i))



while 1:
    print("\n SELECT FROM THE OPTIONS WHICH SPCIALIZATION YOU WANT TO VIEW OR ENTER ANY-KEY TO STOP :")
    for i in resume_all.keys():
        print(" ",i)
    opt=input("ENTER THE NAME :")
    if opt.upper() not in resume_all.keys():
        print(" INVALID ")
        break
    cur_dir=os.path.join(data_dir,opt.upper())
    print("\n SELECT RESUME NAME (without .pdf) YOU WANT TO VIEW OR ENTER ANY-KEY TO STOP :")
    
    for i in os.listdir(cur_dir):
        print(" ",i)

    opt2=input("ENTER THE NAME :")
    opt2 +=".pdf"
    if opt2 not in resume_all[opt.upper()]:
        print(" INVALID ")
        break
    cur_dir=os.path.join(cur_dir,opt2)
    
    all_text=[]
    # Open the PDF file in read-binary mode
    with open(cur_dir, 'rb') as file:
        print(file)
    # Create a PDF object
        pdf = PyPDF2.PdfReader(file)
        text=""
        # Iterate over every page
        for page in pdf.pages:
            # Extract the text from the page
            text += page.extract_text()
            
        all_text.append(text.split(" "))


    # all_text=all_text[0]
    all_text=[x.strip(".") for x in all_text[0]]
    all_text=[x.replace("\n"," ") for x in all_text]
    all_text=[x.strip(",") for x in all_text]
    all_text=[x.split(" ") for x in all_text]
    words=[]
    for i in all_text:
        for j in i:
            if j!="" and j!=":":
                words.append(j.strip(".").strip(",").strip(",").strip(".").lower())
    # Initialize an empty dictionary
    word_counts_hasttable = {} #count using hash table with O(n) time complexity

    # Iterate over the list of words
    for word in words:
        # word=word.lower()
    # If the word is not in the dictionary, add it and set the count to 1
        if word not in word_counts_hasttable:
            word_counts_hasttable[word] = 1
        # If the word is already in the dictionary, increment the count
        else:
            word_counts_hasttable[word] += 1

    # print(word_counts_hasttable)
    
    #using Binary search tree with O(n log n) for BST and searching eith O(log n)
    class Node:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
            self.count = 1

    class BST:
        def __init__(self):
            self.root = None

        def insert(self, val):
            if self.root is None:
                self.root = Node(val)
            else:
                self._insert(val, self.root)

        def _insert(self, val, node):
            if val < node.val:
                if node.left is None:
                    node.left = Node(val)
                else:
                    self._insert(val, node.left)
            elif val > node.val:
                if node.right is None:
                    node.right = Node(val)
                else:
                    self._insert(val, node.right)
            else:
                node.count += 1

        def search(self, val):
            if self.root is None:
                return 0
            else:
                return self._search(val, self.root)

        def _search(self, val, node):
                if val < node.val:
                    if node.left is None:
                        return 0
                    else:
                        return self._search(val, node.left)
                elif val > node.val:
                    if node.right is None:
                        return 0
                    else:
                        return self._search(val, node.right)
                else:
                    return node.count
    def count_occurrences(word, word_list):
            bst = BST()
            for w in word_list:
                bst.insert(w)
            return bst.search(word)
    word_counts_bst = {}
    for word in words:
        word_counts_bst[word]=count_occurrences(word,words) 
    
    # the time complexity adds with O(n log n) + O(n)
    # print(word_counts_bst)


    # for sorting
    # quick sort
    # with  O(n log n) time complexity in average cases 
    def quicksort(hash_map):
        if len(hash_map) <= 1:
            return hash_map
        pivot = hash_map[len(hash_map) // 2]
        left = [x for x in hash_map if x[1] > pivot[1]]
        middle = [x for x in hash_map if x[1] == pivot[1]]
        right = [x for x in hash_map if x[1] < pivot[1]]
        return quicksort(left) + middle + quicksort(right)

    def sort_hash_map(d):
        # Convert the hash map to a list of tuples and sort it using the quicksort function
        sorted_list = quicksort(list(d.items()))
        # Convert the sorted list back to a hash map
        sorted_hash_map = {}
        for key, value in sorted_list:
            sorted_hash_map[key] = value
        return sorted_hash_map
    
    sorted_word_list_ss=sort_hash_map(word_counts_bst)

        

    class Counter(abc.ABC):
        def __init__(self, text):
            self.text = text
            self.word_count = 0

        @abc.abstractmethod
        def count_words(self):
            """Count the words in the text."""
            pass

    class TechnicalWordCounter(Counter):
        def count_words(self,dict_of_words):
            for i in dict_of_words.keys():
                if i in techwords:
                    self.word_count+=dict_of_words[i]

    class NonTechnicalWordCounter(Counter):
        def count_words(self,dict_of_words):
            for i in dict_of_words.keys():
                if i not in techwords:
                    self.word_count+=dict_of_words[i]
    #getting technical words
    print("\n ENTER ALL TECHNICAL WORDS YOU ARE LOOKING FOR WITH SPACES IN BETWEEN 2 WORDS :")
    tec_w=input("ENTER")
    techwords=tec_w.lower().split(" ")

    # Create a reference to the base class
    counter = Counter

    # Create objects of the derived classes using the base class reference
    technical_counter = TechnicalWordCounter("technical")
    nontechnical_counter = NonTechnicalWordCounter("nontechnical")

    # Use the objects to count the occurrence of words in the list
    technical_counter.count_words(sorted_word_list_ss)
    nontechnical_counter.count_words(sorted_word_list_ss)
    print(sorted_word_list_ss) #sorted hash map
    # Display the counts of occurrence of words
    print(f"Number of technical words: {technical_counter.word_count}")
    print(f"Number of non-technical words: {nontechnical_counter.word_count}")





