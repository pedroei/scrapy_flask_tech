import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn import tree


def classification(hundred=100, store=0, term=0, csv_path='../classification/products_scraped.csv'):
    df = pd.read_csv(csv_path)

    inputs = df.drop(columns=['_id', 'id', 'image', 'link', 'price', 'scrape_date_time', 'name', 'scrape_date'])
    target = df['price']

    le_store = LabelEncoder()
    le_term = LabelEncoder()

    inputs['store_n'] = le_store.fit_transform(inputs['store'])
    inputs['term_n'] = le_term.fit_transform(inputs['term'])

    inputs_n = inputs.drop(['store', 'term'], axis='columns')

    model = tree.DecisionTreeClassifier()
    model.fit(inputs_n, target)

    score = model.score(inputs_n, target)
    # prediction = model.predict([[100, 0, 0]])
    prediction = model.predict([[hundred, store, term]])

    print(f"Decision Tree Classification Score: {score}")

    return prediction[0]


def mapping_fields(stores=False, terms=False, csv_path='../classification/products_scraped.csv'):
    df = pd.read_csv(csv_path)

    inputs = df.drop(columns=['_id', 'id', 'image', 'link', 'price', 'scrape_date_time', 'name', 'scrape_date'])

    if (stores is True and terms is True) or (stores is False and terms is False):
        return

    if stores is True:
        le_store = LabelEncoder()
        stores = le_store.fit_transform(inputs['store'])

        mapping_stores = dict(zip(le_store.classes_, range(len(le_store.classes_))))
        all([mapping_stores[x] for x in le_store.inverse_transform(stores)] == stores)  # if it is true, it works

        return mapping_stores

    if terms is True:
        le_term = LabelEncoder()
        terms = le_term.fit_transform(inputs['term'])

        mapping_terms = dict(zip(le_term.classes_, range(len(le_term.classes_))))
        all([mapping_terms[x] for x in le_term.inverse_transform(terms)] == terms)  # if it is true, it works

        return mapping_terms
