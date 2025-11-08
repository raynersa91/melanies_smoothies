# Obter FRUIT_NAME e SEARCH_ON do Snowflake
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'), col('SEARCH_ON')).to_pandas()

# Lista para exibição (FRUIT_NAME) e dicionário para mapeamento
fruit_display_list = my_dataframe['FRUIT_NAME'].tolist()
fruit_map = dict(zip(my_dataframe['FRUIT_NAME'], my_dataframe['SEARCH_ON']))

# Multiselect mostrando FRUIT_NAME (ex.: Apples)
ingredients_list = st.multiselect(
    'choose up to 5 ingredients:',
    fruit_display_list,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')

        # Buscar na API usando SEARCH_ON (ex.: Apple)
        api_name = fruit_map[fruit_chosen]
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + api_name)

        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Inserir no banco usando FRUIT_NAME (como exibido)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


