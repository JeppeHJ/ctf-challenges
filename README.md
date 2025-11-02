This is a collection of various Capture The Flag-challenges I have created.

## Challenges

### BrunnerCTF 2025
- Baking Bad (web)
- Single Slice of CakeNews (web)
- Dat Overflow Dough (pwn)

### Erhvervsakademi Aarhus Introduction to Hacking 2024
- Hack The Fundamentals (boot2root)

## Details
Challenges are stored by category and each challenge has a `src`-folder with the files used to generate and/or host the challenge, and a `solution`-folder with a solve-script and short writeup. *Note: None of these folders are normally available for the solvers.*

If a challenge is meant to have a handout, then that folder will also be found within the challenge-folder. *Note: This folder is normally available for the solvers.*

## Setup

Each challenge has a `docker-compose.yml` that makes hosting the challenge and/or the handout extremely convenient! Simply follow the instructions below and you're all set:
```bash
git clone https://github.com/JeppeHJ/ctf-challenges.git
cd ctf-challenges/DESIRED_CHALLENGE/src
sudo docker compose up
```

The `Hack The Fundamentals` boot2root-challenge has a slightly different - but also convenient - setup outlined in the `README` of that folder.


