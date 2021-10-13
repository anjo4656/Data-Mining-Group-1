import pandas as pd
import networkx
from networkx.algorithms.community.modularity_max import greedy_modularity_communities
from networkx.algorithms.community.centrality import girvan_newman
import networkx.algorithms.community as nx_comm
# rm_main is a mandatory function, 
# the number of arguments has to be the number of input ports (can be none),
#     or the number of input ports plus one if "use macros" parameter is set
# if you want to use macros, use this instead and check "use macros" parameter:
#def rm_main(data,macros):
def rm_main(df):
    df["user_a"] = pd.to_numeric(df["user_a"])
    df["user_b"] = pd.to_numeric(df["user_b"])
    df["fb"] = pd.to_numeric(df["fb"])
    df["bt"] = pd.to_numeric(df["bt"])
    df["sms"] = pd.to_numeric(df["sms"])
    df["calls"] = pd.to_numeric(df["calls"])
    #df["weight"] = pd.to_numeric(df["weight"])
    df.weight = df.weight.astype(float)



    
    G=networkx.from_pandas_edgelist(df=df, source='user_a', target='user_b', edge_attr='weight')
    result = greedy_modularity_communities(G, weight='weight')
    m = nx_comm.modularity(G, result, weight='weight', resolution=1)
    print(m)

    df = weight(df, 0.1, 2, 2, 1)
    G=networkx.from_pandas_edgelist(df=df, source='user_a', target='user_b', edge_attr='weight')
    result = greedy_modularity_communities(G, weight='weight')
    m = nx_comm.modularity(G, result, weight='weight', resolution=1)
    print(m)
    
    
    d = {}
    for cluster in range(0, len(result)):
        for node in list(result[cluster]):
            d[node] = cluster

    networkx.set_node_attributes(G, d, "cluster")
    networkx.write_graphml(G, "G.graphml")
    return df


def weight(df, fb, bt, sms, calls):
    for row in range(0, df.shape[0]):
        df.at[row, 'weight'] = df.at[row, 'fb']*fb + df.at[row, 'bt']*bt + df.at[row, 'sms']*sms + df.at[row, 'calls']*calls

        
        print("weight value:" + str(df.at[row, 'fb']*fb + df.at[row, 'bt']*bt + df.at[row, 'sms']*sms + df.at[row, 'calls']*calls))
        print("weight lookup: " + str(df.at[row, 'weight']))

    return df   
    
