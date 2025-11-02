import os
import asyncio
from fastapi.responses import FileResponse
import httpx
from fastapi import FastAPI
from reactpy import Layout, component, html, use_state, use_effect
from reactpy.backend.fastapi import configure
from reactpy_router import route, browser_router,link
import random


app = FastAPI()


CATEGORIES = ["sports", "business", "technology", "entertainment", "health", "science"]






def render_news_list(news_list):

    return html.div(
        html.p (f"Resultados: {len(news_list)}"),
        
        [
            html.div(
                {"class": "article"},
                [

                    html.img({"src": article["image"], "width": "300px"}) if article["image"] else html.p("no image"),

                    html.div(
                        [
                            html.h2(f"Titulo: {article['title']}"),
                            html.p(f"Publicador: {article['source']}"),
                            html.p(f"Fecha de publicacion: {article['date']}"),
                            html.p(f" Descripcion: {article['description']}") if article["description"] else html.p("no description"),
                            html.a(
                                {
                                    "href": article["url"],
                                    "target": "_blank",
                                },
                                "Abrir articulo",
                            ),
                        ]
                    )
                ]
            )
            for article in news_list
        ] 
    )


async def fetch_news(urlpar):
    async with httpx.AsyncClient() as client:
        url = urlpar
        res = await client.get(f"{url}&pageSize=100&page=1")
        if res.status_code == 200:
            data = res.json()
            articles = data["articles"]
            noticias = []
            for i in articles:
                noticias.append({
                    "title": i["title"],
                    "source": i["source"]["name"],
                    "image": i["urlToImage"],
                    "url": i["url"],
                    "description": i["description"],
                    "date": i["publishedAt"]
                })
            return noticias
        return []




@component
def Navigation():
    is_open, set_is_open = use_state(False)

    return html.div(       
        [
            html.button(
                {
                    "on_click": lambda _: set_is_open(lambda prev: not prev),
                    "class": "toggle-btn"
                },
                "☰" if not is_open else "×"
            ),
            html.nav(
                {"class": f"side-menu {'hidden' if not is_open else ''}"},
                [
                    html.h2("Navigation"),
                    link({"href": "/"}, [html.button("Inicio")]),
                    link({"href": "/search"}, [html.button("Busqueda")]),
                    html.h3("Categorias"),
                    html.div(
                        {"class": "category-container"},
                        *[
                            html.div(
                                link({"href": f"/category-{cat}"}, [html.button(cat.capitalize())])
                            )
                            for cat in CATEGORIES
                        ],
                    ),
                    html.h4("Por si estas aburrido"),
                    link({"href": "/random_article"}, [html.button("Ruleta de articulos")]),
                    link({"href": "/article_time_machine"}, [html.button("Noticias del pasado")]),
                ]
            )
        ],
    )
@component
def homepage():
    home_list, set_home_list = use_state([])


    @use_effect
    def load_news():
        async def task():
            noticias = await fetch_news("https://newsapi.org/v2/top-headlines?country=us&apiKey=[Insert your api key available for free if you create your account in news api]")
            set_home_list(noticias)
        asyncio.create_task(task())


    return html.div(
        {"class": "home"},
        Navigation(),
        html.h1("News-Finder") if home_list else html.h1(""),
        html.h2("Top Headlines"),
        render_news_list(home_list),
        html.p("cargando...")if not home_list else html.p("")
    )

@component
def SearchResults():
    search_list, set_search_list = use_state([])
    query,set_query= use_state("")
    loading, set_loading= use_state(False)

    async def search_news_effect():
        set_loading(True)
        if not query:
            set_search_list([])
            return

        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=popularity&apiKey=[Insert free key after creating account in news api]"
        noticias = await fetch_news(url)
        set_search_list(noticias)
        set_loading(False)

    return html.div(

        {"class": "search"},
        [
        Navigation(),
        html.h1("News-Finder"),
        html.p("(Si al darle a buscar no aparecen resultados es posible que no se hayan encontrado noticias con esos parametros)"),
        html.h2("Busca Noticias"),
        html.input({
            "type": "text",
            "placeholder": "Buscar...",
            "value": query,
            "on_change": lambda event: set_query(event["target"]["value"]) 
        }),
        html.button(
            {
                "on_click": lambda event: asyncio.create_task(search_news_effect())
            },
            "Search"),
        html.h3("Resultados"),
        html.p("Cargando...") if loading else html.p(""),
        render_news_list(search_list),
        ])

@component
def Random_Article():
    random_choice, set_random_choice = use_state(None)
    articles, set_articles= use_state([])
    cycling, set_cycling = use_state(False)
    displayed_article, set_displayed_article = use_state(None)

    @use_effect
    def get_news():
        async def task():
            noticias = await fetch_news("https://newsapi.org/v2/everything?q=news&sortBy=publishedAt&pageSize=100&apiKey=[Insert free key after creating account in news api]")
            if noticias:
                set_articles(noticias)         
        asyncio.create_task(task())
    async def roulette():
        if not articles:
            return
        set_cycling(True)
        for _ in range(20):  
            set_displayed_article(random.choice(articles))
            await asyncio.sleep(0.1)
        chosen = random.choice(articles)
        set_random_choice(chosen)
        set_displayed_article(chosen)
        set_cycling(False)
        
    @use_effect
    def activar_primer_vuelta():
        if articles and not cycling and not random_choice:
            asyncio.create_task(roulette())





    return html.div(
        {"class": "random_article"},
        Navigation(),
        html.h1("News-Finder"),
        html.p("Dale al botón y descubre un artículo elegido al azar"),
        html.button(
            {
                "class": "random-btn",
                "on_click": lambda event: asyncio.create_task(roulette())
            },
            "Mostrar artículo aleatorio"
        ),
        render_news_list([displayed_article]) if random_choice else html.p("Aún no hay artículo aleatorio, dale al boton para generar uno"),
        html.p("cargando...") if not random_choice else html.p("")
    )
    
@component
def Past_Articles():
    articles, set_articles = use_state([])
    year, set_year = use_state("")
    month, set_month = use_state("")
    day, set_day = use_state("")
    loading, set_loading = use_state(False)

    async def fetch_articles():        
        set_loading(True)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key=[Insert free key after creating account in newsyork times developer]"
            )
            data = response.json()
            docs = data["response"]["docs"]
            target_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

            extracted_articles = []
            for doc in docs:
                if doc["pub_date"].startswith(target_date):
                    multimedia = doc["multimedia"]
                    image_url = None
                    for item in multimedia:
                        if item["subtype"] == "xlarge":
                            image_url = f"https://www.nytimes.com/{item['url']}"
                            break
                    if image_url is None and multimedia:
                        image_url = f"https://www.nytimes.com/{multimedia[0]['url']}"

                    extracted_articles.append({
                        "title": doc["headline"]["main"],
                        "url": doc["web_url"],
                        "image": image_url,
                        "date": doc["pub_date"][:10],
                        "description": doc["abstract"],
                        "source": "New York Times"
                    })
        set_articles(extracted_articles)
        set_loading(False)

    return html.div(
        {"class": "articles_date"},
        Navigation(),
        html.h1("News-finder"),
        html.p("Puedes ver los atras en el tiempo hasta la fecha 09/1851 (resultados pueden ser abundantes)"),
        html.div(
            html.p("Quiero ver articulos de"),
                html.input({
                "type": "text",
                "placeholder": "Dia...",
                "value": day,
                "on_input": lambda event: set_day(event["target"]["value"])
            }),
            html.input({
                "type": "text",
                "placeholder": "Mes...",
                "value": month,
                "on_input": lambda event: set_month(event["target"]["value"])
            }),
            html.input({
                "type": "text",
                "placeholder": "Año...",
                "value": year,
                "on_input": lambda event: set_year(event["target"]["value"])
            }),
            html.button(
                {
                    "class": "date-btn",
                    "on_click": lambda event: asyncio.create_task(fetch_articles())
                },
                "Ver Articulos de esa fecha"
            ),
        ),
        html.p("cargando...") if loading else html.p(""),
        render_news_list(articles),

    )

@component
def Category_News(category):
    category_list, set_category_list = use_state([])


    @use_effect
    def load_news():
        async def task():
            noticias = await fetch_news(f"https://newsapi.org/v2/top-headlines?category={category}&apiKey=[Insert free key after creating account in news api]")
            set_category_list(noticias)
        asyncio.create_task(task())

    return html.div(
        {"class": "categories"},
        Navigation(),
        html.h1("News-Finder") if category_list else html.h1(""),
        html.h2(category.capitalize()) if category_list else html.h1(""),
        render_news_list(category_list),
        html.p("cargando...") if not category_list else html.p("")
    )



def make_category_component(category):
    @component
    def CategoryPage():
        return Category_News(category)
    return CategoryPage


@component
def Layout(children):
    return html.div(
        [
            html.link({"rel": "stylesheet", "href": "/styles.css"}),
            children
        ]
    )

@component
def Main():
    static_category_routes = [
        route(f"/category-{cat}", Layout(make_category_component(cat)()))
        for cat in CATEGORIES
    ]

    return browser_router(
        route("/", Layout(homepage())),
        route("/search", Layout(SearchResults())),
        route("/random_article", Layout(Random_Article())),
        route("/article_time_machine", Layout(Past_Articles())),
        *static_category_routes
    )

@app.get("/styles.css")
async def serve_css():
    return FileResponse(os.path.join(os.path.dirname(__file__), "styles.css"))

configure(app, Main)




