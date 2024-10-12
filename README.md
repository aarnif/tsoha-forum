## Keskustelusovellus

Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

## Sovelluksen ominaisuuksia:

- [x] Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- [x] Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
- [x] Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- [x] Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- [x] Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
- [x] Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- [x] Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- [x] Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

## Sovelluksessa käytetyt teknologiat:

- Flask
- PostgreSQL
- HTML
- CSS
- JavaScript
- Ikonit: [Font Awesome](https://fontawesome.com/)

## Sovelluksen demo:

Sovellus on testattavissa:

[https://tsoha-forum.onrender.com](https://tsoha-forum.onrender.com)\
(Palvelimella saattaa kestää useita minuutteja käynnistyä...)

Admin-tunnukset:\
username: admin\
password: password

Peruskäyttäjä-tunnukset:\
username: user1\
password: password

Sovelluksen tietokannassa valmiina oleva data on luotu ChatGPT:llä.

## Sovelluksen testaus paikallisesti:

```
HTTPS - git clone https://github.com/aarnif/tsoha-forum.git

SSH - git clone git@github.com:aarnif/tsoha-forum.git

cd tsoha-forum
```

Luo .env-tiedosto yllä olevan hakemiston juureen ja korvaa alla olevien ympäristömuuttujien arvot omillasi:

```
DATABASE_URL=postgres-tietokannan url
SECRET_KEY=salainen avain
```

Tämän jälkeen:

```
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

flask run
```
