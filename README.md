- [X] Tilføj oberserver pattern - Troels
  - [X] Tilføj console observer - Troels
  - [X] Tilføj Websocket observer - Troels
  - [ ] Tilføj end of round observer (summér resultater over mange hænder) - Troels
- [X] Tilføj tests - Bovle
- [ ] Lav UI - Harder
- [ ] Hjælp til bot udvikling
  - [X] preflop hånd rang 
  - [X] postflop hånd rang
  - [ ] Bedre bot eksempler
- [ ] Håndter multiple kampe samtidig
  - [ ] Spil N bots mod hinanden alle mod alle
  - [ ] Vis resultat som matchup tabel
- [ ] Fejlhåndtering
  - [ ] Hvis de crasher
  - [ ] Hvis de tager for lang tid (1 sekund?)
- [ ] Reimplment scoreboard using Google docs
  - [ ] Gather results (in observer?) 
  - [ ] Upload raw data to Google sheets
  - [ ] Make Google Sheet that displays data in a pretty way

Nice to have:

- [ ] løbende turneringer
  - [ ] Hvordan får vi deres kode?
    - [ ] GitHub gist?
    - [ ] Github Repo?





Challenge:
 - Much faster (10x) with pypy3 (https://www.pypy.org/download.html)


Sort dependencies:
 - `isort -l 120 bots environment utils main.py read_results.py challenge.py`
