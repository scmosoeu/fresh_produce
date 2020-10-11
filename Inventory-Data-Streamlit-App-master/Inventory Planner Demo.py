"""

    Simple Streamlit webserver application for serving developed embedding
    a dashboard visualisation in streamlit.

"""
# Streamlit dependencies
import streamlit as st
#import joblib,os

# Data dependencies
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import pandas as pd
from pulp import *
import math
import base64
from PIL import Image


# The main function where we will build the actual app
def main():
    """Dashboard with Streamlit """

    # Creates a main title and subheader on your page -
    # these are static across all pages
    #st.title("Fresh Produce Inventory Planner")

    # Creating sidebar with selection box -
    # you can create multiple pages this way
    options = ["Trends", "Inventory Planning"]
    selection = st.sidebar.selectbox("Choose Option", options)

    # Building out the "Information" page

    if selection == "Trends":
        #st.info("General Information")
        # You can read a markdown file from supporting resources folder
        #st.subheader("Dashboard")
        #st.subheader("==========================================================")
        #st.subheader("Dashboard Trends")
        #st.subheader("==========================================================")
        @st.cache(allow_output_mutation=True)
        def get_base64_of_bin_file(bin_file):
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()

        def set_png_as_page_bg(png_file):
            bin_str = get_base64_of_bin_file(png_file)
            page_bg_img = '''
            <style>
            body {
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
            }
            </style>
            ''' % bin_str

            st.markdown(page_bg_img, unsafe_allow_html=True)
            return

        #set_png_as_page_bg('Inventory Planning.png')
        st.markdown("""
        <iframe width="1190" height="800" src="https://app.powerbi.com/view?r=eyJrIjoiNzdlNjk3MWItZGVkOC00YzMyLTk1ODEtMGQzYzkxZjk0NDQ5IiwidCI6IjhhZGM0MGUwLWRhMTYtNDBiNC1iZDdjLWJmZDk1ODcxOTQ4NyJ9&pageName=ReportSection" frameborder="0" allowFullScreen="true"></iframe>
        """, unsafe_allow_html=True)

        #st.markdown("""
        #<iframe width="800" height="486" src="https://app.powerbi.com/view?r=eyJrIjoiNDdlZjY1NjYtYTc3MC00YjllLWFhZGMtYWZkZDAzNWZmZTRjIiwidCI6IjhhZGM0MGUwLWRhMTYtNDBiNC1iZDdjLWJmZDk1ODcxOTQ4NyJ9" frameborder="0" allowFullScreen="true"></iframe>
        #""", unsafe_allow_html=True)

    if selection == "Inventory Planning":
        image = Image.open('Inventory Smaller header.png')
        st.image(image, caption=None, use_column_width=True)


        #st.subheader("==========================================================")
        #st.subheader("Inventory Planning")
        #st.subheader("==========================================================")


        #"""### 2) GENERATE DATA"""

        np.random.seed(123)

        def generate_toy_data(n, lam, a, b):
            '''Generate random number from poisson distribution.
            Input:
            n = number of data points to generate
            lam = lambda of the poisson distribution
            a, b = any positive coefficient (since we want to simulate demand)

            Output:
            x = independent variable
            y = demand for toy data that results from a*x + b, with x ~ poisson(lam)
            '''
            x = np.random.poisson(lam, n)
            x = x.reshape((-1,1))

            y = a*x + b
            y = y.reshape((-1,1))
            y = y.astype(int)

            return x, y

            # generate toy data
        demand=st.slider("What level of demand do you expect to have next week?",1.00,100.00,25.00, format="%f percent")/100
        st.markdown ("Expecting low demand: 1%-25% of customers compared to previous week")
        st.write ("Expecting medium demand: 25%-75% of customers compared to previous week")
        st.write ("Expecting high demand: 75%-100% of customers compared to previous week")
        ##high_demand=0.75
        x, y = generate_toy_data(1000, 100, demand,2)

        # visualize toy data
        plt.figure()
        sns.distplot(y)
        plt.show()
        ##st.pyplot()
        #"""### 3) IMPLEMENT SIMPLE PREDICTION"""

        # split data to training and testing set
        train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2)

        df_train = pd.DataFrame({'train_x': train_x.flatten(), 'train_y': train_y.flatten()})
        df_test = pd.DataFrame({'test_x': test_x.flatten(), 'test_y': test_y.flatten()})

        #"""#### a) RANDOM FOREST"""

        rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
        rf.fit(train_x, train_y)

        test_y_rfpred = (rf.predict(test_x)).astype(int)
        err_rf = abs(test_y_rfpred - test_y)
        print("Mean Absolute Error:", round(np.mean(err_rf), 2), "degrees.")

        #"""#### b) LINEAR REGRESSION"""

        lr = LinearRegression()
        lr.fit(train_x, train_y)

        test_y_lrpred = (rf.predict(test_x)).astype(int)
        err_lr = abs(test_y_lrpred - test_y)
        print('Mean Absolute Error:', round(np.mean(err_lr), 2), 'degrees.')

        # check coefficient
        print(lr.coef_)
        print(lr.intercept_)

        #"""#### c) SUMMARIZE RESULT & CHECK GRAPH (RANDOM FOREST & LINREG)"""

        df_summ = pd.DataFrame({'test_x': test_x.flatten(),
                                'test_y': test_y.flatten(),
                                'test_y_rfpred': test_y_rfpred.flatten(),
                                'test_y_lrpred': test_y_lrpred.flatten()})
        df_summ['diff_rf_actual'] = df_summ['test_y_rfpred'] - df_summ['test_y']
        df_summ['diff_lr_actual'] = df_summ['test_y_lrpred'] - df_summ['test_y']

        # toy data is simple, hence prediction is rather powerful as we only have few missed prediction
        # even so, in this kind of cases:
        # --> we will lose potential profit if prediction < demand
        # --> we will incur unnecessary cost if prediction > demand as we cannot sell the remaining goods at selling price
        #df_summ[(df_summ['diff_rf_actual'] != 0) | (df_summ['diff_lr_actual'] != 0)]

        plt.figure()

        components = [test_y, test_y_rfpred, test_y_lrpred]
        labels=['test_y', 'test_y_rfpred', 'test_y_lrpred']

        fig, axes = plt.subplots(1)
        for component in components:
            sns.distplot(component)

        axes.legend(labels=labels)
        plt.show()
        #st.pyplot(fig)

        #"""### 4) STOCHASTIC PROGRAMMING
        #### a) DISCRETIZING DEMAND: TO CAPTURE PROBABILITY OF EACH POSSIBLE SCENARIO
        #"""

        # capturing probability of each possible scenario can be done in many ways,
        # ranging from simple descriptive analytics to more complicated things like
        # moment matching, monte carlo simulation, etc.
        # we do the easiest here: do clustering to generate scenario (max 100 scenario for now)

        def cluster_1d(df, max_cluster=100):
            '''Cluster data into n different cluster where n is the minimum between unique scenario and max_cluster.
            Input:
            df = dataframe column containing scenario to cluster
            max_cluster = number of maximum cluster we want to have (default=100)

            Output:
            cluster_centers_df = mapping between cluster labels and its centers
            cluster_labels_df = mapping between df and its cluster labels
            '''
            km = KMeans(n_clusters=min(len(df.unique()),max_cluster))
            km.fit(df.values.reshape(-1,1))

            # get information about center
            cluster_centers_df = pd.DataFrame(np.array(km.cluster_centers_.reshape(1,-1)[0].tolist()))
            cluster_centers_df.columns = ['cluster_centers']
            cluster_centers_df['labels'] = range(len(cluster_centers_df))

            # get information about labels and add information about center
            cluster_labels_df = pd.DataFrame(np.array(km.labels_))
            cluster_labels_df.columns = ['labels']
            cluster_labels_df = pd.concat([df.reset_index(drop=True), cluster_labels_df], axis=1)
            cluster_labels_df = pd.merge(cluster_labels_df, cluster_centers_df, on='labels', how='left')

            return cluster_centers_df, cluster_labels_df

        def cluster_summ(df):
            '''Summarize probability for each scenario by referring to result from cluster_1d.
            Input:
            df = dataframe column containing scenario to cluster

            Output:
            cluster_proportion_df = dataframe containing complete information about probability for each scenario
            demand = possible scenario to happen
            weight = probability of the possible scenario to happen
            scenarios = indexing for demand
            '''
            cluster_centers_df, cluster_labels_df = cluster_1d(df)

            count_label = cluster_labels_df[['labels']].count().values[0]
            cluster_proportion_df = cluster_labels_df[['cluster_centers', 'labels']].groupby('cluster_centers').count().reset_index(drop=False)
            cluster_proportion_df['count_labels'] = count_label
            cluster_proportion_df['proportion_labels'] = cluster_proportion_df['labels'] / cluster_proportion_df['count_labels']
            cluster_proportion_df['index'] = range(1,cluster_proportion_df.shape[0] + 1)
            cluster_proportion_df['cluster_centers'] = np.round(cluster_proportion_df['cluster_centers'], decimals=(3))

            demand = pd.Series(cluster_proportion_df['cluster_centers'].values, index=cluster_proportion_df['index'].values).to_dict()
            weight = pd.Series(cluster_proportion_df['proportion_labels'].values, index=cluster_proportion_df['index'].values).to_dict()
            scenarios = range(1,len(cluster_proportion_df.cluster_centers.values)+1)

            return cluster_proportion_df, demand, weight, scenarios

        cluster_proportion_df, demand, weight, scenarios = cluster_summ(df=df_train['train_y'])

        print(demand)
        print(weight)
        print(scenarios)
        #"""#### b) USING PULP TO SOLVE STOCHASTIC PROGRAMMING"""


        N = st.number_input("How many stock items are you able to purchase next week?",10)         # maximum item to purchase
        #st.slider(N, 0, 100)
        cost_price = st.number_input("Forecasted cost price to be paid to the to be supplier for each stock item for this specific product selection, size, and class?",1.00) # amount paid to the supplier
        sell_price = st.number_input("Forecasted customer retail selling price for stock item?",1.00) # amount paid by the customer
        waste_price = 0 # amount paid if we sell the remaining goods (ie. when we have more stock as prediction > demand)

        ##########################################
        # DEFINE VARIABLES
        ##########################################

        M = LpProblem("Newsvendor1", LpMaximize)

        x = LpVariable('x', lowBound=0)
        z = LpVariable.dicts('z', scenarios, 0)


        ##########################################
        # DEFINE MODELS: CONSTRAINTS
        ##########################################

        for i in scenarios:
            print(demand[i])
            print(weight[i])
            M += x <= N
            M += z[i] <= x
            M += z[i] <= demand[i]


        ##########################################
        # DEFINE MODELS: OBJECTIVE
        ##########################################

        M += sum(weight[i] * (sell_price * z[i] + waste_price * (x - z[i])) for i in scenarios) - (cost_price * x)
        M.solve()


        ##########################################
        # PRINT RESULTS
        ##########################################

        print("Status = %s" % LpStatus[M.status])

        print("%s = %f" % (x.name, x.varValue))
        for i in scenarios:
            print("%s = %f" % (z[i].name, z[i].varValue))
        print("Objective = %f" % (M.objective.value()))

        #"""#### c) CHECK AS TABLE (MANUAL CALCULATION): TO SEE CLEARLY WHAT HAPPENS"""

        def result_summ(cluster_proportion_df, demand, weight, sell_price, cost_price, waste_price):
            '''Summarize result by comparing possible scenario (example_df) with its possible execution (purchase_df).
            We want to look how much profit we can get given a pair of scenario and its execution,
            weighted with the probability of each scenario to happen.
            Input:
            cluster_proportion_df = dataframe containing complete information about probability for each scenario
            demand = possible scenario to happen
            weight = probability of the possible scenario to happen
            cost_price = amount paid to the supplier
            sell_price = amount paid by the customer
            waste_price = amount paid if we sell the remaining goods

            Output:
            example_df = dataframe after cross join between possible scenario and possible execution
            example_df_summ = summary of example_df to obtain total expected profit per possible execution
            '''

            # get the basic df: purchase_df for the demand and example_df for the possible scenario execution
            purchase_df = pd.DataFrame({'key': 0, 'item_to_purchase': demand})
            example_df = pd.DataFrame({'key': 0, 'item_to_sell': cluster_proportion_df['cluster_centers'],
                                       'probability': cluster_proportion_df['proportion_labels']})
            example_df = example_df.merge(purchase_df, on='key', how='outer')
            example_df = example_df.drop('key', axis=1).sort_values(['item_to_purchase', 'item_to_sell'])

            example_df['total_revenue'] = example_df[['item_to_sell', 'item_to_purchase']].min(axis=1) * sell_price
            example_df['total_cost'] = example_df['item_to_purchase'] * cost_price
            example_df['total_profit'] = (example_df['total_revenue'] - example_df['total_cost'])

            example_df['total_weighted_profit'] = example_df['probability'] * example_df['total_profit']
            example_df['total_cumsum_profit'] = example_df.groupby('item_to_purchase')['total_weighted_profit'].cumsum()

            example_df_summ = example_df.groupby('item_to_purchase', as_index=False)['total_weighted_profit'].sum()

            return example_df, example_df_summ

        example_df, example_df_summ = result_summ(cluster_proportion_df=cluster_proportion_df, demand=demand, weight=weight,
                                                  sell_price=sell_price, cost_price=cost_price, waste_price=waste_price)
        #example_df

        #"""#### d) VISUAL CHECK"""

        # limit the table, we don't want to be overwhelmed
        temp = example_df[(example_df['item_to_purchase'] >= 20) & (example_df['item_to_purchase'] <= 25)]
        temp.loc[:,'item_to_purchase'] = temp['item_to_purchase'].astype('str')

        # check the weighted profit per possible scenario:
        # we can see how higher execution causes greater loss during weak demand and hence,
        # higher execution number has difficulty in bouncing the profit up

        fig1, ax = plt.subplots()

        for i in temp['item_to_purchase'].unique():
            temp[temp['item_to_purchase'] == i].plot.line(x='item_to_purchase', y='total_weighted_profit', ax=ax, label=str(i))
        plt.xticks(range(0,np.unique(temp['item_to_sell']).shape[0]),np.unique(temp['item_to_sell']),rotation=45)
        plt.show()

        # check the total expected profit, which comes from all possible profit
        # and weighted by the probability of the scenario to happen
        #fig = plt.figure(figsize=(4,3))
        fig, ax = plt.subplots()
        plt.scatter(x='item_to_purchase', y='total_weighted_profit', data=example_df_summ)
        ax.set_xlabel('Optimal stock count for item')
        ax.set_ylabel('Profit range for item (Rands)')
        ax.set_title('Inventory profit scenarios visualisation')
        plt.show()
        st.pyplot(fig)

        #"""### 5) PREDICTION + STOCHASTIC PROGRAMMING
        #### a) BOOTSTRAPPING
        #"""
        from math import floor
        size_bstrap = N
        iter = math.floor(N/2)
        idx_check = 172
        test_y_bstrap = []
        coef_bstrap = []
        intercept_bstrap = []

        for i in range(iter):

            # sampling with replacement
            idx = np.random.choice(np.arange(0,train_x.shape[0]), size_bstrap, replace=True)
            train_x_temp = train_x[idx]
            train_y_temp = train_y[idx]

            # do linear regression
            lr_bstrap = LinearRegression()
            lr_bstrap.fit(train_x_temp, train_y_temp)

            # get coefficient and intercept
            coef_bstrap.append(lr_bstrap.coef_)
            intercept_bstrap.append(lr_bstrap.intercept_)

            # get result, only for intended index idx_check
            # test_y_bstrap.append((lr_bstrap.predict(test_x)[idx_check][0]).astype(int))
            result_temp = np.rint(lr_bstrap.intercept_ + lr_bstrap.coef_ * test_x[idx_check])[0,0]
            test_y_bstrap.append(result_temp)

        result_bstrap = pd.DataFrame({'test_y_bstrap': test_y_bstrap})
        result_bstrap['test_x_bstrap'] = test_x[idx_check][0]
        #result_bstrap

        result_bstrap_summ = result_bstrap.groupby('test_y_bstrap').count().reset_index(drop=False)
        #result_bstrap_summ

        #"""#### b) DISCRETIZING DEMAND"""

        cluster_proportion_df_bstrap, demand_bstrap, weight_bstrap, scenarios_bstrap = cluster_summ(df=result_bstrap['test_y_bstrap'])

        print(demand_bstrap)
        print(weight_bstrap)
        print(scenarios_bstrap)

        #"""#### c) USING PULP TO SOLVE STOCHASTIC PROGRAMMING"""

        ##########################################
        # DEFINE VARIABLES
        ##########################################

        M_bstrap = LpProblem("Newsvendor2", LpMaximize)

        x_bstrap = LpVariable('x_bstrap', lowBound=0)
        z_bstrap = LpVariable.dicts('z_bstrap', scenarios_bstrap, 0)


        ##########################################
        # DEFINE MODELS: CONSTRAINTS
        ##########################################

        for i in scenarios_bstrap:
            print(demand_bstrap[i])
            print(weight_bstrap[i])
            M_bstrap += x_bstrap <= N
            M_bstrap += z_bstrap[i] <= x_bstrap
            M_bstrap += z_bstrap[i] <= demand_bstrap[i]


        ##########################################
        # DEFINE MODELS: OBJECTIVE
        ##########################################

        M_bstrap += sum(weight_bstrap[i] * (sell_price * z_bstrap[i] + waste_price * (x_bstrap - z_bstrap[i])) for i in scenarios_bstrap) - (cost_price * x_bstrap)
        M_bstrap.solve()


        ##########################################
        # PRINT RESULTS
        ##########################################

        print("Status = %s" % LpStatus[M_bstrap.status])

        print("%s = %f" % (x_bstrap.name, x_bstrap.varValue))
        for i in scenarios_bstrap:
            print("%s = %f" % (z_bstrap[i].name, z_bstrap[i].varValue))
        print("Objective = %f" % (M_bstrap.objective.value()))

        #"""#### d) CHECK AS TABLE (MANUAL CALCULATION): TO SEE CLEARLY WHAT HAPPENS"""

        example_df_bstrap, example_df_summ_bstrap = result_summ(cluster_proportion_df=cluster_proportion_df_bstrap,
                                                                demand=demand_bstrap, weight=weight_bstrap,
                                                                sell_price=sell_price, cost_price=cost_price,
                                                                waste_price=waste_price)
        example_df_bstrap.head(n=5)

        # optimal decision will only change if we increase sales_price (eg. sales_price = 23)
        example_df_bstrap, example_df_summ_bstrap = result_summ(cluster_proportion_df=cluster_proportion_df_bstrap,
                                                                demand=demand_bstrap, weight=weight_bstrap,
                                                                sell_price=sell_price, cost_price=cost_price,
                                                                waste_price=waste_price)
        example_df_bstrap.head(n=5)

        #"""#### d) VISUAL CHECK"""

        example_df_bstrap.loc[:,'item_to_purchase'] = example_df_bstrap['item_to_purchase'].astype('str')

        # check the weighted profit per possible scenario:
        # we can see how higher execution causes greater loss during weak demand and hence,
        # higher execution number has difficulty in bouncing the profit up

        #fig, ax = plt.subplots()

        #for i in example_df_bstrap['item_to_purchase'].unique():
            #example_df_bstrap[example_df_bstrap['item_to_purchase'] == i].plot.line(x='item_to_purchase', y='total_weighted_profit', ax=ax, label=str(i))
        #plt.xticks(range(0,np.unique(example_df_bstrap['item_to_sell']).shape[0]),np.unique(example_df_bstrap['item_to_sell']),rotation=45)
        #plt.show()

        # check the total expected profit, which comes from all possible profit
        # and weighted by the probability of the scenario to happen
        #plt.figure()
        #sns.scatterplot(x='item_to_purchase', y='total_weighted_profit', data=example_df_summ_bstrap)
        #plt.show()

# Required to let Streamlit instantiate our web app.
if __name__ == '__main__':
    main()
