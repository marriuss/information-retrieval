GAMES = \
    {
        "kb": "Kings Bounty 1, 2",
        "h1": "Heroes of Might and Magic",
        "h2": "Heroes of Might and Magic II",
        "h3": "Heroes of Might and Magic III",
        "h3w": "Heroes of Might and Magic WoG",
        "h3h": "Heroes of Might and Magic HotA",
        "h4": "Heroes of Might and Magic IV",
        "h4e": "Heroes of Might and Magic IV Equilibris",
        "h5": "Heroes of Might and Magic V",
    }


def parse_article(page, url, groups):
    version, article_type = groups
    game = GAMES[version]
    article = page.select("div#article_content")
    if not article:
        return
    text = text_preprocessing(article[0].text)
    return {
        "url": url,
        "game": game,
        "article_title": article_type,
        "article_text": text
    }


def parse_map(page, url, groups):
    map_info = page.select("div.map-info")[0]
    name = map_info.select("h2.name")[0].text
    game = map_info.select("div.map-game")[0].text
    rating = int(map_info.select("span#rating")[0].text)
    main_info = map_info.select("dl.info.main")[0]
    info = main_info.find_all("dd")
    size = info[0].text
    author = info[1].text
    humans = int(info[2].text)
    language = info[3].text
    teams = int(info[4].text)
    comments = info[5].text.replace(" (оставить)", "")
    comments_amount = 0 if comments == "нет" else int(comments)
    players = int(info[6].text)
    downloads = int(info[7].text)
    date = info[8].text
    likes, dislikes = map(int, info[10].text.split(" / "))
    description_div = map_info.select("div.description")
    description = None
    if description_div:
        description = description_div[0].text.replace(' — описание карты.', '')
        description = text_preprocessing(description)
    return {
        "url": url,
        "name": name,
        "description": description,
        "author": author,
        "date": date,
        "language": language,
        "game": game,
        "size": size,
        "players": players,
        "humans": humans,
        "teams": teams,
        "rating": rating,
        "downloads": downloads,
        "likes": likes,
        "dislikes": dislikes,
        "comments": comments_amount,
    }


def parse_profile(page, url, groups):
    profile_info = page.select("div.c.f_h")[0]
    nickname = profile_info.select("span#nick")[0].text
    if nickname == "Not found":
        return
    block_right = profile_info.select("div#block_right")[0]
    block_right_subblocks_big = block_right.select("div.subblock_big")
    info = block_right_subblocks_big[0]
    parameters = info.select("div.c_parameter")
    id = None
    gender = None
    birth_date = None
    country = None
    language = None
    registration_date = None
    for p in parameters:
        name = p.select("div.name")[0].text
        value = p.select("div.value")[0]
        match name:
            case "ID":
                id = int(value.text)
            case "Пол":
                gender = value.contents[0].attrs["title"]
            case "Дата рождения":
                birth_date = string2date(value.text.strip())
            case "Страна проживания":
                if not value.select("img"):
                    country = value.text
                else:
                    country = value.select("img")[0].attrs["title"]
                if country == "Неизвестно":
                    country = None
            case "Язык":
                language = value.text
            case "Дата регистрации":
                registration_date = string2date(value.text.strip())
            case _:
                pass
    points = None
    points_div = profile_info.select("div.points")
    if points_div:
        points = float(points_div[0].text.replace(" @", ""))
    return {
        "url": url,
        "nickname": nickname,
        "id": id,
        "gender": gender,
        "birth_date": birth_date,
        "country": country,
        "language": language,
        "registration_date": registration_date,
        "points": points,
    }


def parse_disabled_clan(page, url, groups):
    content = page.select("div.content")[0]
    title = content.select("h2")[0].text
    info = content.select("dl.info.wide")[0]
    start_date = None
    end_date = None
    leader = None
    if info:
        parameters = info.find_all("dd")
        parametrs_amount = len(parameters)
        if parametrs_amount >= 1:
            start_date = string2date(parameters[0].text.replace(".г.", ""))
        if parametrs_amount >= 2:
            end_date = string2date(parameters[1].text.replace(".г.", ""))
        if parametrs_amount >= 3:
            leader = parameters[2].text
    members = None
    members_list = content.select("dl.exposition.member>dt")
    if members_list:
        members = [m.text for m in members_list]
    rules = None
    rules_ol = content.select("div.common-box>ol")
    if rules_ol:
        rules = text_preprocessing(rules_ol[0].text)
    return {
        "url": url,
        "title": title,
        "start_date": start_date,
        "end_date": end_date,
        "leader": leader,
        "members": members,
        "rules": rules,
    }


def parse_active_clan(page, url, groups):
    content = page.select("div.c.f_h")[0]
    title = content.select("div.name")[0].text
    members = None
    members_list = content.select("div.nick")
    if members_list:
        members = [m.text for m in members_list]
    rules = None
    rules_div = content.select("div#information")
    if rules_div:
        rules = text_preprocessing(rules_div[0].text)
    return {
        "url": url,
        "title": title,
        "members": members,
        "rules": rules,
    }


def string2date(string_date):
    dict = {
        "января": "01",
        "февраля": "02",
        "марта": "03",
        "апреля": "04",
        "мая": "05",
        "июня": "06",
        "июля": "07",
        "августа": "08",
        "сентября": "09",
        "октября": "10",
        "ноября": "11",
        "декабря": "12",
    }
    date = string_date.lower().replace(" ", ".")
    for m in dict:
        if m in string_date:
            date = date.replace(m, dict[m])
    return date


def text_preprocessing(text):
    import re
    text = re.sub(r'[\d\t\n\r\f\v(\xa0)\."!\?;,:%\+/\[\]*\'=\(\)]', ' ', text)
    text = re.sub(r'(\w+)- ', lambda m: f'{m.groups()[0]} ', text)
    text = re.sub(r' -(\w+)', lambda m: f' {m.groups()[0]}', text)
    text = re.sub(r' [-–—] ', ' ', text)
    text = re.sub(r'( +)', ' ', text)
    text = text.lower().strip()
    return text


PARSING_FUNCTIONS = {
    "map": parse_map,
    "profile": parse_profile,
    "active_clan": parse_active_clan,
    "disabled_clan": parse_disabled_clan,
    "article": parse_article,
}
