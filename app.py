#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## DASH APPLICATION CODE

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Load the data
file = pd.read_csv('https://raw.githubusercontent.com/ajsCDSA1040/RestaurantRecommender/main/entree.csv')

def combined_features(row):
    return row["RestaurantAttributes"]
file["combined_features"] = file.apply(combined_features, axis=1)

cv = CountVectorizer()
count_matrix = cv.fit_transform(file["combined_features"])
cos_sim = cosine_similarity(count_matrix)

def get_index(name):
    return file[file["RestaurantName"] == name]["Index"].values[0]
def get_restaurant(index):
    return file[file["Index"] == index]["RestaurantName"].values[0]
def get_restaurant_city(index):
    return file[file["Index"] == index]["RestaurantCity"].values[0]

#Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#111111',
    'text': 'firebrick'
}

#Build the layout
app.layout = html.Div([
    html.H1("Entree Chicago",style={
        'textAlign': 'left-center',
        'color': colors['text'],
        'fontWeight': 'bold',
        }),
    
    html.Div([
    dcc.Dropdown(
        id='user',
        placeholder='Are you a new user?',
        options=[{'label': 'Yes', 'value': 'Yes'},
            {'label': 'No', 'value': 'No'}],
        value='',
        style={'width': 300, 'textAlign': 'left-center'})
    ],
        className='row'),
    
    html.Br(),
    
    dcc.Input(
        id='userid',
        placeholder='Enter your User ID',
        type='number',
        value='',
        style={'width': 300}
    ), 
    
    html.Br(),
    html.Br(),
    
    dcc.Input(
        id='restaurant',
        placeholder='Enter your favourite restaurant',
        type='text',
        value='',
        style={'width': 300}
    ),
    html.Button('Submit', id='button', n_clicks=0),
    html.H6("The top 10 recommended restaurants in Chicago are: "),
    html.Div(id='output', style={'whiteSpace': 'pre-line'})
])

@app.callback(
    Output('output', 'children'),
    Input('user', 'value'),
    Input('userid', 'value'),
    Input('button', 'n_clicks'),
    State('restaurant', 'value')
)

#If the user is new, restaurant recommendations will be based on the features of the inputted restaurant 
def update_output(user, userid, n_clicks, restaurant):
    if user == "Yes":
        if n_clicks > 0:
            restaurant_index = get_index(restaurant)
            similiar_restaurants = list(enumerate(cos_sim[restaurant_index]))
            sorted_restaurants = sorted(similiar_restaurants,key=lambda x:x[1],reverse=True)
        
            top_matched = []
            for i in sorted_restaurants:
                if i[1] > 0.1:
                    top_matched.append(i[0])
                
            recommended_restaurants = []
            for i in top_matched:
                recommended_restaurant_cities = []
                recommended_restaurant_cities.append(get_restaurant_city(i))
                for item in recommended_restaurant_cities:
                    if item == "Chicago":
                        recommended_restaurants.append(get_restaurant(i))
        
            if restaurant in file.values:
                return html.Ul([html.Li(recommended_restaurants[0]), 
                            html.Li(recommended_restaurants[1]),
                            html.Li(recommended_restaurants[2]),
                            html.Li(recommended_restaurants[3]),
                            html.Li(recommended_restaurants[4]),
                            html.Li(recommended_restaurants[5]),
                            html.Li(recommended_restaurants[6]),
                            html.Li(recommended_restaurants[7]),
                            html.Li(recommended_restaurants[8]),
                            html.Li(recommended_restaurants[9]),
                           ])
#If the user is returning, restaurant recommendations will be based on past user selections
    else:
        # Read ratings file
        ratings = pd.read_csv('https://raw.githubusercontent.com/ajsCDSA1040/RestaurantRecommender/main/session2.csv')

        df = pd.DataFrame(ratings, columns = ['UserID','000000C','000001C','000002C','000003C','000004C','000005C','000006C','000007C','000008C','000009C','0000010C','0000011C','0000012C','0000013C','0000014C','0000015C','0000016C','0000017C','0000018C','0000019C','0000020C','0000021C','0000022C','0000023C','0000024C','0000025C','0000026C','0000027C','0000028C','0000029C','0000030C','0000031C','0000032C','0000033C','0000034C','0000035C','0000036C','0000037C','0000038C','0000039C','0000040C','0000041C','0000042C','0000043C','0000044C','0000045C','0000046C','0000047C','0000048C','0000049C','0000050C','0000051C','0000052C','0000053C','0000054C','0000055C','0000056C','0000057C','0000058C','0000059C','0000060C','0000061C','0000062C','0000063C','0000064C','0000065C','0000066C','0000067C','0000068C','0000069C','0000070C','0000071C','0000072C','0000073C','0000074C','0000075C','0000076C','0000077C','0000078C','0000079C','0000080C','0000081C','0000082C','0000083C','0000084C','0000085C','0000086C','0000087C','0000088C','0000089C','0000090C','0000091C','0000092C','0000093C','0000094C','0000095C','0000096C','0000097C','0000098C','0000099C','00000100C','00000101C','00000102C','00000103C','00000104C','00000105C','00000106C','00000107C','00000108C','00000109C','00000110C','00000111C','00000112C','00000113C','00000114C','00000115C','00000116C','00000117C','00000118C','00000119C','00000120C','00000121C','00000122C','00000123C','00000124C','00000125C','00000126C','00000127C','00000128C','00000129C','00000130C','00000131C','00000132C','00000133C','00000134C','00000135C','00000136C','00000137C','00000138C','00000139C','00000140C','00000141C','00000142C','00000143C','00000144C','00000145C','00000146C','00000147C','00000148C','00000149C','00000150C','00000151C','00000152C','00000153C','00000154C','00000155C','00000156C','00000157C','00000158C','00000159C','00000160C','00000161C','00000162C','00000163C','00000164C','00000165C','00000166C','00000167C','00000168C','00000169C','00000170C','00000171C','00000172C','00000173C','00000174C','00000175C','00000176C','00000177C','00000178C','00000179C','00000180C','00000181C','00000182C','00000183C','00000184C','00000185C','00000186C','00000187C','00000188C','00000189C','00000190C','00000191C','00000192C','00000193C','00000194C','00000195C','00000196C','00000197C','00000198C','00000199C','00000200C','00000201C','00000202C','00000203C','00000204C','00000205C','00000206C','00000207C','00000208C','00000209C','00000210C','00000211C','00000212C','00000213C','00000214C','00000215C','00000216C','00000217C','00000218C','00000219C','00000220C','00000221C','00000222C','00000223C','00000224C','00000225C','00000226C','00000227C','00000228C','00000229C','00000230C','00000231C','00000232C','00000233C','00000234C','00000235C','00000236C','00000237C','00000238C','00000239C','00000240C','00000241C','00000242C','00000243C','00000244C','00000245C','00000246C','00000247C','00000248C','00000249C','00000250C','00000251C','00000252C','00000253C','00000254C','00000255C','00000256C','00000257C','00000258C','00000259C','00000260C','00000261C','00000262C','00000263C','00000264C','00000265C','00000266C','00000267C','00000268C','00000269C','00000270C','00000271C','00000272C','00000273C','00000274C','00000275C','00000276C','00000277C','00000278C','00000279C','00000280C','00000281C','00000282C','00000283C','00000284C','00000285C','00000286C','00000287C','00000288C','00000289C','00000290C','00000291C','00000292C','00000293C','00000294C','00000295C','00000296C','00000297C','00000298C','00000299C','00000300C','00000301C','00000302C','00000303C','00000304C','00000305C','00000306C','00000307C','00000308C','00000309C','00000310C','00000311C','00000312C','00000313C','00000314C','00000315C','00000316C','00000317C','00000318C','00000319C','00000320C','00000321C','00000322C','00000323C','00000324C','00000325C','00000326C','00000327C','00000328C','00000329C','00000330C','00000331C','00000332C','00000333C','00000334C','00000335C','00000336C','00000337C','00000338C','00000339C','00000340C','00000341C','00000342C','00000343C','00000344C','00000345C','00000346C','00000347C','00000348C','00000349C','00000350C','00000351C','00000352C','00000353C','00000354C','00000355C','00000356C','00000357C','00000358C','00000359C','00000360C','00000361C','00000362C','00000363C','00000364C','00000365C','00000366C','00000367C','00000368C','00000369C','00000370C','00000371C','00000372C','00000373C','00000374C','00000375C','00000376C','00000377C','00000378C','00000379C','00000380C','00000381C','00000382C','00000383C','00000384C','00000385C','00000386C','00000387C','00000388C','00000389C','00000390C','00000391C','00000392C','00000393C','00000394C','00000395C','00000396C','00000397C','00000398C','00000399C','00000400C','00000401C','00000402C','00000403C','00000404C','00000405C','00000406C','00000407C','00000408C','00000409C','00000410C','00000411C','00000412C','00000413C','00000414C','00000415C','00000416C','00000417C','00000418C','00000419C','00000420C','00000421C','00000422C','00000423C','00000424C','00000425C','00000426C','00000427C','00000428C','00000429C','00000430C','00000431C','00000432C','00000433C','00000434C','00000435C','00000436C','00000437C','00000438C','00000439C','00000440C','00000441C','00000442C','00000443C','00000444C','00000445C','00000446C','00000447C','00000448C','00000449C','00000450C','00000451C','00000452C','00000453C','00000454C','00000455C','00000456C','00000457C','00000458C','00000459C','00000460C','00000461C','00000462C','00000463C','00000464C','00000465C','00000466C','00000467C','00000468C','00000469C','00000470C','00000471C','00000472C','00000473C','00000474C','00000475C','00000476C','00000477C','00000478C','00000479C','00000480C','00000481C','00000482C','00000483C','00000484C','00000485C','00000486C','00000487C','00000488C','00000489C','00000490C','00000491C','00000492C','00000493C','00000494C','00000495C','00000496C','00000497C','00000498C','00000499C','00000500C','00000501C','00000502C','00000503C','00000504C','00000505C','00000506C','00000507C','00000508C','00000509C','00000510C','00000511C','00000512C','00000513C','00000514C','00000515C','00000516C','00000517C','00000518C','00000519C','00000520C','00000521C','00000522C','00000523C','00000524C','00000525C','00000526C','00000527C','00000528C','00000529C','00000530C','00000531C','00000532C','00000533C','00000534C','00000535C','00000536C','00000537C','00000538C','00000539C','00000540C','00000541C','00000542C','00000543C','00000544C','00000545C','00000546C','00000547C','00000548C','00000549C','00000550C','00000551C','00000552C','00000553C','00000554C','00000555C','00000556C','00000557C','00000558C','00000559C','00000560C','00000561C','00000562C','00000563C','00000564C','00000565C','00000566C','00000567C','00000568C','00000569C','00000570C','00000571C','00000572C','00000573C','00000574C','00000575C','00000576C','00000577C','00000578C','00000579C','00000580C','00000581C','00000582C','00000583C','00000584C','00000585C','00000586C','00000587C','00000588C','00000589C','00000590C','00000591C','00000592C','00000593C','00000594C','00000595C','00000596C','00000597C','00000598C','00000599C','00000600C','00000601C','00000602C','00000603C','00000604C','00000605C','00000606C','00000607C','00000608C','00000609C','00000610C','00000611C','00000612C','00000613C','00000614C','00000615C','00000616C','00000617C','00000618C','00000619C','00000620C','00000621C','00000622C','00000623C','00000624C','00000625C','00000626C','00000627C','00000628C','00000629C','00000630C','00000631C','00000632C','00000633C','00000634C','00000635C','00000636C','00000637C','00000638C','00000639C','00000640C','00000641C','00000642C','00000643C','00000644C','00000645C','00000646C','00000647C','00000648C','00000649C','00000650C','00000651C','00000652C','00000653C','00000654C','00000655C','00000656C','00000657C','00000658C','00000659C','00000660C','00000661C','00000662C','00000663C','00000664C','00000665C','00000666C','00000667C','00000668C','00000669C','00000670C','00000671C','00000672C','00000673C','00000674C','00000675C'])

        melted_ratings = pd.melt(df,id_vars=['UserID'],
                        value_vars=['000000C','000001C','000002C','000003C','000004C','000005C','000006C','000007C','000008C','000009C','0000010C','0000011C','0000012C','0000013C','0000014C','0000015C','0000016C','0000017C','0000018C','0000019C','0000020C','0000021C','0000022C','0000023C','0000024C','0000025C','0000026C','0000027C','0000028C','0000029C','0000030C','0000031C','0000032C','0000033C','0000034C','0000035C','0000036C','0000037C','0000038C','0000039C','0000040C','0000041C','0000042C','0000043C','0000044C','0000045C','0000046C','0000047C','0000048C','0000049C','0000050C','0000051C','0000052C','0000053C','0000054C','0000055C','0000056C','0000057C','0000058C','0000059C','0000060C','0000061C','0000062C','0000063C','0000064C','0000065C','0000066C','0000067C','0000068C','0000069C','0000070C','0000071C','0000072C','0000073C','0000074C','0000075C','0000076C','0000077C','0000078C','0000079C','0000080C','0000081C','0000082C','0000083C','0000084C','0000085C','0000086C','0000087C','0000088C','0000089C','0000090C','0000091C','0000092C','0000093C','0000094C','0000095C','0000096C','0000097C','0000098C','0000099C','00000100C','00000101C','00000102C','00000103C','00000104C','00000105C','00000106C','00000107C','00000108C','00000109C','00000110C','00000111C','00000112C','00000113C','00000114C','00000115C','00000116C','00000117C','00000118C','00000119C','00000120C','00000121C','00000122C','00000123C','00000124C','00000125C','00000126C','00000127C','00000128C','00000129C','00000130C','00000131C','00000132C','00000133C','00000134C','00000135C','00000136C','00000137C','00000138C','00000139C','00000140C','00000141C','00000142C','00000143C','00000144C','00000145C','00000146C','00000147C','00000148C','00000149C','00000150C','00000151C','00000152C','00000153C','00000154C','00000155C','00000156C','00000157C','00000158C','00000159C','00000160C','00000161C','00000162C','00000163C','00000164C','00000165C','00000166C','00000167C','00000168C','00000169C','00000170C','00000171C','00000172C','00000173C','00000174C','00000175C','00000176C','00000177C','00000178C','00000179C','00000180C','00000181C','00000182C','00000183C','00000184C','00000185C','00000186C','00000187C','00000188C','00000189C','00000190C','00000191C','00000192C','00000193C','00000194C','00000195C','00000196C','00000197C','00000198C','00000199C','00000200C','00000201C','00000202C','00000203C','00000204C','00000205C','00000206C','00000207C','00000208C','00000209C','00000210C','00000211C','00000212C','00000213C','00000214C','00000215C','00000216C','00000217C','00000218C','00000219C','00000220C','00000221C','00000222C','00000223C','00000224C','00000225C','00000226C','00000227C','00000228C','00000229C','00000230C','00000231C','00000232C','00000233C','00000234C','00000235C','00000236C','00000237C','00000238C','00000239C','00000240C','00000241C','00000242C','00000243C','00000244C','00000245C','00000246C','00000247C','00000248C','00000249C','00000250C','00000251C','00000252C','00000253C','00000254C','00000255C','00000256C','00000257C','00000258C','00000259C','00000260C','00000261C','00000262C','00000263C','00000264C','00000265C','00000266C','00000267C','00000268C','00000269C','00000270C','00000271C','00000272C','00000273C','00000274C','00000275C','00000276C','00000277C','00000278C','00000279C','00000280C','00000281C','00000282C','00000283C','00000284C','00000285C','00000286C','00000287C','00000288C','00000289C','00000290C','00000291C','00000292C','00000293C','00000294C','00000295C','00000296C','00000297C','00000298C','00000299C','00000300C','00000301C','00000302C','00000303C','00000304C','00000305C','00000306C','00000307C','00000308C','00000309C','00000310C','00000311C','00000312C','00000313C','00000314C','00000315C','00000316C','00000317C','00000318C','00000319C','00000320C','00000321C','00000322C','00000323C','00000324C','00000325C','00000326C','00000327C','00000328C','00000329C','00000330C','00000331C','00000332C','00000333C','00000334C','00000335C','00000336C','00000337C','00000338C','00000339C','00000340C','00000341C','00000342C','00000343C','00000344C','00000345C','00000346C','00000347C','00000348C','00000349C','00000350C','00000351C','00000352C','00000353C','00000354C','00000355C','00000356C','00000357C','00000358C','00000359C','00000360C','00000361C','00000362C','00000363C','00000364C','00000365C','00000366C','00000367C','00000368C','00000369C','00000370C','00000371C','00000372C','00000373C','00000374C','00000375C','00000376C','00000377C','00000378C','00000379C','00000380C','00000381C','00000382C','00000383C','00000384C','00000385C','00000386C','00000387C','00000388C','00000389C','00000390C','00000391C','00000392C','00000393C','00000394C','00000395C','00000396C','00000397C','00000398C','00000399C','00000400C','00000401C','00000402C','00000403C','00000404C','00000405C','00000406C','00000407C','00000408C','00000409C','00000410C','00000411C','00000412C','00000413C','00000414C','00000415C','00000416C','00000417C','00000418C','00000419C','00000420C','00000421C','00000422C','00000423C','00000424C','00000425C','00000426C','00000427C','00000428C','00000429C','00000430C','00000431C','00000432C','00000433C','00000434C','00000435C','00000436C','00000437C','00000438C','00000439C','00000440C','00000441C','00000442C','00000443C','00000444C','00000445C','00000446C','00000447C','00000448C','00000449C','00000450C','00000451C','00000452C','00000453C','00000454C','00000455C','00000456C','00000457C','00000458C','00000459C','00000460C','00000461C','00000462C','00000463C','00000464C','00000465C','00000466C','00000467C','00000468C','00000469C','00000470C','00000471C','00000472C','00000473C','00000474C','00000475C','00000476C','00000477C','00000478C','00000479C','00000480C','00000481C','00000482C','00000483C','00000484C','00000485C','00000486C','00000487C','00000488C','00000489C','00000490C','00000491C','00000492C','00000493C','00000494C','00000495C','00000496C','00000497C','00000498C','00000499C','00000500C','00000501C','00000502C','00000503C','00000504C','00000505C','00000506C','00000507C','00000508C','00000509C','00000510C','00000511C','00000512C','00000513C','00000514C','00000515C','00000516C','00000517C','00000518C','00000519C','00000520C','00000521C','00000522C','00000523C','00000524C','00000525C','00000526C','00000527C','00000528C','00000529C','00000530C','00000531C','00000532C','00000533C','00000534C','00000535C','00000536C','00000537C','00000538C','00000539C','00000540C','00000541C','00000542C','00000543C','00000544C','00000545C','00000546C','00000547C','00000548C','00000549C','00000550C','00000551C','00000552C','00000553C','00000554C','00000555C','00000556C','00000557C','00000558C','00000559C','00000560C','00000561C','00000562C','00000563C','00000564C','00000565C','00000566C','00000567C','00000568C','00000569C','00000570C','00000571C','00000572C','00000573C','00000574C','00000575C','00000576C','00000577C','00000578C','00000579C','00000580C','00000581C','00000582C','00000583C','00000584C','00000585C','00000586C','00000587C','00000588C','00000589C','00000590C','00000591C','00000592C','00000593C','00000594C','00000595C','00000596C','00000597C','00000598C','00000599C','00000600C','00000601C','00000602C','00000603C','00000604C','00000605C','00000606C','00000607C','00000608C','00000609C','00000610C','00000611C','00000612C','00000613C','00000614C','00000615C','00000616C','00000617C','00000618C','00000619C','00000620C','00000621C','00000622C','00000623C','00000624C','00000625C','00000626C','00000627C','00000628C','00000629C','00000630C','00000631C','00000632C','00000633C','00000634C','00000635C','00000636C','00000637C','00000638C','00000639C','00000640C','00000641C','00000642C','00000643C','00000644C','00000645C','00000646C','00000647C','00000648C','00000649C','00000650C','00000651C','00000652C','00000653C','00000654C','00000655C','00000656C','00000657C','00000658C','00000659C','00000660C','00000661C','00000662C','00000663C','00000664C','00000665C','00000666C','00000667C','00000668C','00000669C','00000670C','00000671C','00000672C','00000673C','00000674C','00000675C'],
                        var_name='restaurant',value_name='rating')

        # Read restaurant file
        restaurants_text = pd.read_csv('https://raw.githubusercontent.com/ajsCDSA1040/RestaurantRecommender/main/chicago_restaurants.csv')

        Restaurant_Rating_df = pd.merge(restaurants_text, melted_ratings, on = 'restaurant')

        # Pivot ratings into restaurant features
        user_data = Restaurant_Rating_df.pivot(index = 'UserID', columns = 'RestaurantName', values = 'rating').fillna(0)

        # Make a copy of dataset
        dummy_train = Restaurant_Rating_df.copy()
        dummy_train['rating'] = dummy_train['rating'].apply(lambda x: 0 if x > 0 else 1)

        # The restaurants not rated by user is marked as 1 for prediction 
        dummy_train = dummy_train.pivot(index = 'UserID', columns = 'RestaurantName', values = 'rating').fillna(1)

        restaurant_features = Restaurant_Rating_df.pivot(index = 'RestaurantName', columns = 'UserID', values = 'rating').fillna(0)


        # Item Similarity Matrix using Cosine similarity as a similarity measure between Items
        item_similarity = cosine_similarity(restaurant_features)
        item_similarity[np.isnan(item_similarity)] = 0

        ### Predicting the User ratings on the restaurants
        item_predicted_ratings = np.dot(restaurant_features.T, item_similarity)

        # np.multiply for cell-by-cell multiplication 
        item_final_ratings = np.multiply(item_predicted_ratings, dummy_train)
        
        if userid in ratings.values:
            finalratings1 = item_final_ratings.iloc[userid].sort_values(ascending = False)[0:10]
            finalratings2 = finalratings1[1:10]
            finalratings3 = finalratings1[2:10]
            finalratings4 = finalratings1[3:10]
            finalratings5 = finalratings1[4:10]
            finalratings6 = finalratings1[5:10]
            finalratings7 = finalratings1[6:10]
            finalratings8 = finalratings1[7:10]
            finalratings9 = finalratings1[8:10]
            finalratings10 = finalratings1[9:10]
            return html.Ul([html.Li(finalratings1.idxmax()),
                            html.Li(finalratings2.idxmax()),
                            html.Li(finalratings3.idxmax()),
                            html.Li(finalratings4.idxmax()),
                            html.Li(finalratings5.idxmax()),
                            html.Li(finalratings6.idxmax()),
                            html.Li(finalratings7.idxmax()),
                            html.Li(finalratings8.idxmax()),
                            html.Li(finalratings9.idxmax()),
                            html.Li(finalratings10.idxmax()),
                           ])
        
if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:




