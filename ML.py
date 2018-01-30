from sklearn.tree import DecisionTreeClassifier , export_graphviz
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

treeC = DecisionTreeClassifier()
iris = load_iris()
training_data , test_data , training_target , test_target = train_test_split(iris.data , iris.target , test_size = 0.2)
print (training_data)
print("training target" , training_target)

treeC.fit(training_data, training_target)

result = treeC.predict(test_data)
print("Result: " , result)

for i,j in zip(result , test_target):
    print("Predicted: " , i , "Expected",j)

acc = accuracy_score(test_target,result)
print(acc)

"""
dot_data = export_graphviz(treeC ,out_file = "tree.dot" , node_ids = True)
c = 0
for i in range(len(test_target)):
    if test_target[i]!=result[i]:
        c+=1
        print("for the entry"+str(i)+":"+str(test_data[i]))
        p=treeC.decision_path(test_data[i])
        print(p)
    print(c)

"""

