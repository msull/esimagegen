import streamlit as st
from duckduckgo_search import DDGS

st.set_page_config(layout="wide")


@st.cache_data()
def get_result(search_type, query) -> list[dict | str]:
    results = ["answer"]
    with DDGS() as ddgs:
        match search_type:
            case "text":
                print(f"Searching for text {query=}")
                results = ddgs.text(
                    query,
                    region="wt-wt",
                    safesearch="on",
                    backend="api",
                    max_results=10,
                )
            case "answers":
                print(f"Searching for answers {query=}")
                results = ddgs.answers(query)
            case "news":
                print(f"Searching for news {query=}")
                results = ddgs.news(
                    query,
                    region="wt-wt",
                    safesearch="on",
                    max_results=10,
                )
            case "images":
                print(f"Searching for images {query=}")
                results = ddgs.images(
                    query,
                    region="wt-wt",
                    safesearch="on",
                    size=None,
                    # color="Monochrome",
                    type_image=None,
                    layout=None,
                    license_image=None,
                    max_results=12,
                )
            case "videos":
                print(f"Searching for videos {query=}")
                results = ddgs.videos(
                    query,
                    region="wt-wt",
                    safesearch="on",
                    max_results=10,
                )
            case "maps":
                pass
            case "translate":
                pass
            case "suggestions":
                results = ddgs.suggestions(query)
            case _:
                raise ValueError("Unhandled search type")
        return list(results)


def main():
    with st.container(border=True):
        with st.form("search", border=False):
            c1, c2 = st.columns((1, 3))
            with c1:
                search_type = st.selectbox(
                    "type",
                    [
                        "text",
                        "answers",
                        "news",
                        "images",
                        "videos",
                        "maps",
                        "translate",
                        "suggestions",
                    ],
                )
            with c2:
                query = st.text_input("search", "")
            with c1:
                if st.form_submit_button("Submit"):
                    if not (search_type and query):
                        st.error("Submit a query")
                        st.stop()
                    st.session_state.search_type = search_type
                    st.session_state.query = query
                    st.session_state.search_results = get_result(search_type, query)
        show_operators = st.toggle("Show DDG search operators")

    if show_operators:
        st.write(
            """
| Keywords example         | Result                                                     |
|--------------------------|------------------------------------------------------------|
| cats dogs                | Results about cats or dogs                                 |
| "cats and dogs"          | Results for exact term "cats and dogs". If no results are found, related results are shown. |
| cats -dogs               | Fewer dogs in results                                      |
| cats +dogs               | More dogs in results                                       |
| cats filetype\:pdf       | PDFs about cats. Supported file types: pdf, doc(x), xls(x), ppt(x), html |
| dogs site\:example.com   | Pages about dogs from example.com                          |
| cats -site\:example.com  | Pages about cats, excluding example.com                    |
| intitle\:dogs            | Page title includes the word "dogs"                        |
| inurl\:cats              | Page url includes the word "cats"                          |
        """.strip()
        )
        st.write("\n")

    if search_results := st.session_state.get("search_results"):
        query = st.session_state.query.replace(":", "\:")
        st.write(
            f"**{st.session_state.search_type.capitalize()} Results for `{query}`**"
        )
        match search_type:
            case "text":
                for idx, text in enumerate(search_results):
                    if idx > 0:
                        st.divider()
                    st.subheader(text["title"])
                    st.caption(text["href"])
                    st.write(text["body"])
            case "news":
                for idx, news in enumerate(
                    sorted(search_results, key=lambda x: x["date"], reverse=True)
                ):
                    if idx > 0:
                        st.divider()
                    (
                        c1,
                        c2,
                    ) = st.columns((2, 1))
                    with c1:
                        st.subheader(news["title"])
                        st.caption(news["date"])
                        st.caption(news["url"])
                        st.write(news["body"])
                    with c2:
                        if image := news.get("image"):
                            st.image(image)
            case "videos":
                for idx, video in enumerate(search_results):
                    if idx > 0:
                        st.divider()
                    # st.caption(image["title"])
                    st.link_button(video["title"], video["content"])
                    if images := video.get("images"):
                        st.image(images["large"])
                        if motion := images.get("motion"):
                            st.video(motion)
            case "images":
                for idx, image in enumerate(search_results):
                    if idx > 0:
                        st.divider()
                    st.caption(image["title"])
                    st.image(image["image"])
            case _:
                st.write(search_results)


def main2():
    st.chat_message("ai").write("Hello, Everett")

    st.text_input("Type your message here", key="user_query")

    if st.session_state.user_query:
        st.write(f"__Image results for `{st.session_state.user_query}`__")
        result = get_result("images", st.session_state.user_query)

        num_columns = 4
        columns = iter(st.columns(num_columns, vertical_alignment="bottom"))
        for idx, image in enumerate(result):
            if idx % num_columns == 0:
                columns = iter(st.columns(num_columns, vertical_alignment="bottom"))
            column = next(columns)
            with column:
                st.image(image["image"])
                st.caption(image["title"])


if __name__ == "__main__":
    main2()
