import pandas


# Generates an edge list. For each pair of users a and b that have any
# kind of connection, the edge has the following attributes:
# ['user_a', 'user_b', 'fb', 'bt', 'sms', 'calls', 'weight']
#  - fb: 1 if user a and b are facebook friends, 0 otherwise
#  - sms: The number of sms sent between user a and b
#  - calls: The total number of seconds that user a and b have been calling each other
# TODO: CALCULATE THE REMAINING ATTRIBUTES
def rm_main(fbFriends, gender, bt, sms, calls):
    
    maxID = maxUserID(fbFriends, gender, bt, sms, calls)

    # A list where edges[i] is a data frame containing
    edges = []
    for user in range(0, maxID):
        c =['user_a', 'user_b', 'fb', 'bt', 'sms', 'calls', 'weight']
        userEdges = pandas.DataFrame(columns = c)
        edges.append(userEdges)

    fbEdges(fbFriends, edges)
    smsEdges(sms, edges)
    callsEdges(calls, edges)
    btEdges(bt, edges)
    
    df = edges[0]
    for i in range(1, maxID):
        df = df.append(edges[i], ignore_index=True)

    return df

# Processes the calls. For every call between user a and b that
# lasts t seconds, the edge between user 
# a and b will get +t in the 'calls' column
def btEdges(bt, edges):
    for row in range(0, bt.shape[0]):
        user_a = bt.at[row, 'user_a']
        user_b = bt.at[row, 'user_b']
        rssi = bt.at[row, 'rssi']

        if (user_a == user_b or user_b==-1 or rssi == 0 or user_a == -2 or user_b==-2):
            continue
        distance = 10 ** ((-60 -(rssi))/(10 * 2))
        if distance <= 5:
	        lesser = min(user_a, user_b)
	        greater = max(user_a, user_b)
	        addEdge(edges, lesser, greater, 'bt', 1)

# Processes the calls. For every call between user a and b that
# lasts t seconds, the edge between user 
# a and b will get +t in the 'calls' column
def callsEdges(calls, edges):
    for row in range(0, calls.shape[0]):
        caller = calls.at[row, 'caller']
        callee = calls.at[row, 'callee']
        duration = calls.at[row, 'duration']

        if (caller == callee):
            continue
        if (duration < 0):
        	  continue
        lesser = min(caller, callee)
        greater = max(caller, callee)
        addEdge(edges, lesser, greater, 'calls', duration)

# Processes the sms data. For every message between user a and b,
# no matter who is the sender and recipient, the edge between user 
# a and b will get +1 in the 'sms' column
def smsEdges(sms, edges):
    for row in range(0, sms.shape[0]):
        sender = sms.at[row, 'sender']
        recipient = sms.at[row, 'recipient']

        if (sender == recipient):
            continue

        lesser = min(sender, recipient)
        greater = max(sender, recipient)
        addEdge(edges, lesser, greater, 'sms', 1)    

    
# Processes the Facebook friendships. There is a friendship
# between user a and b, the edge between a and b will get +1
# in the fb column
def fbEdges(fbFriends, edges):
    for row in range(0, fbFriends.shape[0]):
        userA = fbFriends.at[row, 'user_a']
        userB = fbFriends.at[row, 'user_b']

        if (userA == userB):
            continue

        lesser = min(userA, userB)
        greater = max(userA, userB)
        addEdge(edges, lesser, greater, 'fb', 1)


def column_contribution(column):
    return {
        'fb':1, 
        'bt':1,
        'sms':1,
        'calls': 1
    }[column]


# Adds a relation between two users to edges
#  - If those users already have a connecting edge, the values of the edge are modified. 
#    The provided value is added to the correct attribute column of the edge.
#  - Otherwise a new edge is created
#
# EXAMPLE:
# Add edge(a, b, fb, 1) to a set of edges where an edge between a and b
#  - Does not exist: edge (a, b, 1, 0, 0, 0, 0) is added
#  - Exists as (a, b, 0, 2, 3, 4, 5): the existing edge is modified to
#    (a, b, 0+1, 2, 3, 4, 5)
def addEdge(edges, userA, userB, columnLabel, value):
    userEdges = edges[userA]
    rowUserB = userEdges.index[userEdges['user_b']==userB].tolist()

    if (len(rowUserB) == 0):
        newRow = {'user_a': userA, 'user_b': userB, 'fb':0, 'bt':0, 
        'sms':0, 'calls': 0, 'weight':0}
        edges[userA] = edges[userA].append(newRow, ignore_index=True)
        rowUserB = edges[userA].index[edges[userA]['user_b']==userB].tolist()
    
    row = rowUserB[0]
    edges[userA].at[row, columnLabel] += value
    edges[userA].at[row, 'weight'] += column_contribution(columnLabel)*value
      

# Gets the index of a column in 
# ['user_a', 'user_b', 'fb', 'bt' 'sms', 'calls']
def labelIndex(columnLabel):
    if (columnLabel == 'fb'):
        return 2
    elif (columnLabel == 'bt'):
        return 3
    elif (columnLabel == 'sms'):
        return 4
    elif (columnLabel == 'calls'):
        return 5       
    elif (columnLabel == 'weight'):
        return 6        


# Gets the maximum user ID among all the data. 
def maxUserID(fbFriends, gender, bt, sms, calls):
    maxUserFB = max(fbFriends['user_a'].max(), fbFriends['user_b'].max())
    maxUserGender = gender['user'].max()
    maxUserBT = max(bt['user_a'].max(), bt['user_b'].max())
    maxUserSMS = max(sms['sender'].max(), sms['recipient'].max())
    maxUserCalls = max(calls['caller'].max(), calls['callee'].max())

    return max(maxUserFB, maxUserGender, maxUserBT, maxUserSMS, maxUserCalls)



"""
# first test function
def rm_main(gender, fbFriends):

    users = gender.shape[0]

    (friendRows, friendColumns) = fbFriends.shape

    d = {'user': [], 'friends': []}
    df = pandas.DataFrame(data=d)
    df['friends'] = df['friends'].astype('object')
    

    currentUser = fbFriends.at[0, 'user_a']
    currentFriends = []
    for edge in range(0, friendRows):
        nextUser = fbFriends.at[edge, 'user_a']
        if nextUser != currentUser:
            df.at[currentUser, 'user'] = currentUser
            df.at[currentUser, 'friends'] = currentFriends #copy?
            currentUser = nextUser
            currentFriends = []
            
        currentFriends.append(fbFriends.at[edge, 'user_b'])

        if edge == friendRows - 1:
            df.at[currentUser, 'user'] = currentUser
            df.at[currentUser, 'friends'] = currentFriends #copy?

    return df
"""

