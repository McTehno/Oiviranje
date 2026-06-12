# Zagon backenda

Backend je zgrajen s FastAPI in se zažene kot lokalni API strežnik.

## 1. Premik v mapo `backend`

Najprej se premakni v mapo `backend`:

```powershell
cd backend
```

## 2. Ustvarjanje virtualnega okolja

Če virtualno okolje še ne obstaja, ga ustvari z ukazom:

```powershell
python -m venv .venv
```

## 3. Aktivacija virtualnega okolja

V PowerShell terminalu zaženi:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Po uspešni aktivaciji se mora v terminalu prikazati:

```text
(.venv)
```

## 4. Namestitev odvisnosti

```powershell
python -m pip install fastapi uvicorn pydantic requests python-multipart
```

Paket `python-multipart` je potreben za endpoint-e, ki uporabljajo nalaganje datotek oziroma `Form` podatke.

## 5. Zagon backend strežnika

Backend API se nahaja v datoteki:

```text
backend/app/api.py
```

Zato se strežnik zažene z ukazom:

```powershell
python -m uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
```

Če je zagon uspešen, se v terminalu prikaže nekaj podobnega:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## 6. Dostop do API-ja

Backend je nato dostopen na naslovu:

```text
http://127.0.0.1:8000
```

Swagger dokumentacija je dostopna na:

```text
http://127.0.0.1:8000/docs
```

