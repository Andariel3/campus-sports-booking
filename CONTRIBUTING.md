# Cum lucram in repo

Regulile de mai jos sunt pentru toata echipa (backend, frontend, baza de date).

## Pe scurt

- Nu lucram direct pe `main`. Orice modificare ajunge pe `main` doar printr-un pull request.
- Un branch pentru fiecare task. Un task odata.
- Commit-uri mici, fiecare cu o singura schimbare.
- Fiecare PR e vazut de cel putin un coleg inainte de merge.

## Fluxul pentru un task

1. Iei task-ul din Jira dupa ce te-ai inteles cu echipa si il treci pe "in lucru".
2. Iti aduci `main` la zi:

   ```bash
   git checkout main
   git pull
   ```

3. Faci un branch nou din `main`:

   ```bash
   git checkout -b feat/nume-scurt-task
   ```

4. Lucrezi si faci commit-uri mici:

   ```bash
   git add <fisiere>
   git commit -m "rutele pentru rezervari"
   ```

5. Urci branch-ul si deschizi un PR spre `main`:

   ```bash
   git push -u origin feat/nume-scurt-task
   ```

6. Ceri review de la un coleg. Daca primesti comentarii, faci commit-uri noi pe acelasi branch,
   PR-ul se actualizeaza singur.
7. Dupa aprobare faci merge, iti aduci `main` la zi si verifici ca aplicatia merge in continuare.
8. Treci task-ul pe "finalizat" in Jira si incepi urmatorul de la pasul 2.

## Numele branch-urilor

`<tip>/<descriere-scurta>`, cu litere mici si cratime:

| Tip      | Cand                                    | Exemplu                        |
| -------- | --------------------------------------- | ------------------------------ |
| `feat/`  | functionalitate noua                    | `feat/rezervari-crud`          |
| `fix/`   | rezolvare de bug                        | `fix/validare-capacitate`      |
| `chore/` | configurari, dependinte, structura      | `chore/actualizare-fastapi`    |
| `docs/`  | documentatie                            | `docs/contributing`            |
| `test/`  | doar teste                              | `test/facilities-edge-cases`   |

## Mesajele de commit

- scurte, la obiect, cu litere mici, fara diacritice
- spun ce face commit-ul, nu cum: `rutele /api/facilities`, `scheme pydantic pentru facility`
- un commit = o schimbare; daca mesajul are nevoie de "si" de mai multe ori, imparte-l

## Pull request

- titlu scurt cu ce aduce PR-ul (ex. `crud pentru terenuri in backend`)
- in descriere: ce s-a facut, cum se testeaza, de ce PR depinde (daca e cazul)
- PR-uri mici, usor de citit; un PR = un task
- inainte de a cere review: codul ruleaza local si testele trec

## Review

- cel putin o aprobare de la un coleg inainte de merge
- comentariile se rezolva cu commit-uri noi pe acelasi branch
- cine a facut review-ul verifica si ca se respecta stilul de cod al echipei

## Stilul de cod

- **backend (Python):** [PEP 8](https://pep8.org/), verificat cu `ruff`

  ```bash
  cd backend
  ruff check .
  ruff format .
  pytest
  ```

- **frontend (TypeScript/React):** stilul ales de echipa de frontend, trecut si in Confluence la
  "Coding style frontend"

## Ce nu urcam in repo

- fisiere `.env` (avem `.env.example` pentru fiecare)
- `node_modules/`, `.venv/`, build-uri, fisiere generate
- parole, chei, token-uri
