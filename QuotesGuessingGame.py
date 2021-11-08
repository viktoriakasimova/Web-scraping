import requests
from bs4 import BeautifulSoup
from random import choice

ORIG_URL = "http://quotes.toscrape.com"

def get_quotes():
    quotes = []
    url = "/page/1"
    while url:
        response = requests.get(ORIG_URL + url)
        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.select(".quote")
        for item in data:
            quote = item.find(class_="text").get_text()
            name = item.find(class_="author").get_text()
            link = item.find("a")["href"]
            quotes.append({
                "text": quote,
                "author": name,
                "bio-link": link
            })
        next_page = soup.select(".next")
        if next_page:
            url = next_page[0].find("a")["href"]
        else:
            url = None
    return quotes

def play_game(quotes):
    quote = choice(quotes)
    print("Here's a quote:\n")
    print(quote["text"] + "\n")
    guesses = 4
    answer = ""
    while answer.lower() != quote["author"].lower() and guesses > 0:
        answer = input(f"Who said this? Guesses remaining: {guesses}. ")
        if answer.lower() == quote["author"].lower():
            print("You guessed correctly! Congratulations!")
            break
        guesses -= 1
        if guesses == 3:
            response = requests.get(ORIG_URL + quote["bio-link"])
            soup = BeautifulSoup(response.text, "html.parser")
            birth_date = soup.select(".author-born-date")[0].get_text()
            birth_place = soup.select(".author-born-location")[0].get_text()
            print(f"Here's a hint: The author was born on {birth_date} {birth_place}.")
        elif guesses == 2:
            first_init = quote['author'][0]
            print(f"The author's first name starts with {first_init}.")
        elif guesses == 1:
            last_init = quote["author"].split(" ")[-1][0]
            print(f"The author's last name starts with {last_init}.")
        else:
            print(f"Sorry, you lost the game. That was {quote['author']}.")

    again = ""
    while again.lower() not in ("y", "yes", "n", "no"):
        again = input("Would you like to play again (y/n)? ")
    if again.lower() in ("n", "no"):
        print("\nThank you for the game, goodbye!")
    else:
        print("\nGreat! Here we go again...\n")
        return play_game(quotes)

quotes = get_quotes()
play_game(quotes)

