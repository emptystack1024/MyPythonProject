import re

a = int(input())
for _ in range(a):
    s = input()
    list1 = re.findall(r"rock|scissors|paper",s)
    print(list1)
    # length = len(list1)//2
    # win = 0
    # for i in range(length):
    #     if list1[2*i] == "rock":
    #         if list1[2*i+1] == "scissors":
    #             win += 1
    #         elif list1[2*i+1] == "paper":
    #             win -= 1
    #     elif list1[2*i] == "scissors":
    #         if list1[2*i+1] == "rock":
    #             win -= 1
    #         elif list1[2*i+1] == "paper":
    #             win += 1
    #     elif list1[2*i] == "paper":
    #         if list1[2*i+1] == "rock":
    #             win += 1
    #         elif list1[2*i+1] == "scissors":
    #             win -= 1
    # if win == 0:
    #     print("Tie")
    # elif win > 0:
    #     print("Win")
    # else:
    #     print("Lose")