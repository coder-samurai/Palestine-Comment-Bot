# 📣 Instagram Comment Bot voor Palestina 🇵🇸

Een volledig geautomatiseerde, feature-rijke Instagram commenting bot gebouwd met Python en Selenium.  
**Uitsluitend voor educatieve doeleinden** - Geherstructureerd met schone code praktijken, gebruiksvriendelijke configuratie en geavanceerde automatisering functies.

> ⚠️ Deze tool is ontwikkeld **om bewustzijn te ondersteunen voor de mensen van Gaza en Palestina** door krachtige berichten te versterken via Instagram comments.

---

## ✊ Doel

Dit project is gemaakt met een duidelijk doel:  
Om **digitaal verzet te ondersteunen** en **bewustzijn te verspreiden** voor Palestina tijdens tijden van censuur en stilte.

Door hashtags zoals `#FreePalestine`, `#GazaUnderAttack`, en `#SavePalestine`, zorgt deze bot ervoor dat **jouw boodschap blijft** gezien en gehoord worden, zelfs wanneer handmatige inspanning niet genoeg is.

> 🛑 Deze tool is niet gemaakt om haat of spam te verspreiden. Het is een **vreedzame vorm van digitaal activisme**.

---

## 🚀 **NIEUWE Functies - Volledig Gerefactored**

### 🎮 **Interactieve Controle**
- **Console Commando's**: `status`, `stats`, `pause`, `resume`, `stop`, `quit`
- **Telegram Remote Control**: Bestuur bot vanaf overal via `/status`, `/pause`, `/resume` commando's
- **Real-time Statistieken**: Bekijk dagelijkse comment aantallen per account
- **Graceful Shutdown**: Juiste exit handling met signaal management

### ⚙️ **Gebruiksvriendelijke Configuratie**
- **Interactieve Setup**: `python main.py --setup` voor begeleide configuratie
- **JSON Configuratie**: Alle instellingen opgeslagen in `bot_config.json`
- **Geen Code Bewerking**: Configureer alles via prompts of config bestand

### 🌐 **Geavanceerd Proxy Management**
- **Snelheidstest**: Automatisch langzame proxies overslaan (configureerbare latency drempel)
- **Slimme Rotatie**: Alleen geverifieerde snelle proxies gebruiken
- **On-demand Testing**: Proxies alleen getest wanneer nodig
- **Fallback Systeem**: Mislukte proxies opnieuw proberen bij tijdelijke problemen

### 📱 **Telegram Integratie**
- **Notificaties**: Real-time logging naar Telegram
- **Remote Commando's**: Bestuur bot via Telegram berichten
- **Status Rapporten**: Gedetailleerde bot status op afstand
- **Statistieken**: Bekijk comment stats via Telegram

### 🔒 **Verbeterde Beveiliging & Betrouwbaarheid**
- **Cookie Persistentie**: Slim sessie management
- **Dagelijkse Limieten**: Per-account comment limieten (configureerbaar)
- **Duplicaat Preventie**: Nooit twee keer commentaar op dezelfde post
- **Error Recovery**: Robuuste error handling en retry mechanismen

---

## 📁 **Vereiste Bestanden**

### `accounts.txt`
```
gebruikersnaam1:wachtwoord1  
gebruikersnaam2:wachtwoord2  
gebruikersnaam3:wachtwoord3
```

### `comments.txt`
```
🇵🇸 Vrij Palestina  
Gerechtigheid voor Gaza.  
أنقذوا أطفال فلسطين  
اللهم انصر أهل غزة
#FreePalestine ❤️
Sta achter Palestina 🇵🇸
```

### `proxyscrape_premium_http_proxies.txt` (Optioneel)
```
192.168.1.1:8080
10.0.0.1:3128
proxy.example.com:3128
```

### `chromedriver.exe`
Download van [ChromeDriver](https://chromedriver.chromium.org/) en plaats in projectmap.

---

## 🛠️ **Setup & Installatie**

### 1. **Installeer Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Initiële Setup**
```bash
python main.py --setup
```
Dit begeleidt je door:
- Dagelijkse limieten en timing instellingen
- Bestandspad configuratie  
- Proxy instellingen (timeout, snelheidslimieten)
- Browser instellingen (headless mode)
- Telegram bot setup (optioneel)
- Doel hashtags

### 3. **Alternatieve Setup Methoden**
```bash
# Maak voorbeeld config bestand om handmatig te bewerken
python main.py --create-config

# Toon help en alle opties
python main.py --help

# Run met bestaande configuratie
python main.py
```

---

## ⚙️ **Configuratie Opties**

Alle instellingen zijn aanpasbaar via `bot_config.json`:

### 📊 **Limieten & Timing**
- `daily_limit_per_account`: Max comments per account per dag (standaard: 200)
- `min_delay_between_comments`: Minimale wachttijd tussen comments (420s = 7min)
- `max_delay_between_comments`: Maximale wachttijd tussen comments (480s = 8min)
- `min_comments_per_session`: Minimale comments per sessie (2)
- `max_comments_per_session`: Maximale comments per sessie (5)

### 🌐 **Proxy Instellingen**
- `use_proxy`: Proxy rotatie in-/uitschakelen
- `proxy_timeout`: Verbinding timeout in seconden (5s)
- `max_proxy_latency`: Sla proxies langzamer dan dit over (3000ms)
- `proxy_file`: Pad naar proxy bestand

### 📱 **Telegram Integratie**
- `telegram_token`: Bot token van @BotFather
- `telegram_chat_id`: Jouw chat ID voor notificaties
- `enable_telegram_logging`: Auto-ingeschakeld wanneer token + chat ID opgegeven
- `enable_telegram_commands`: Remote control via Telegram

### 🎯 **Targeting**
- `hashtags`: Lijst van hashtags om te targeten
- `max_posts_per_hashtag`: Posts om te controleren per hashtag (50)
- `max_scroll_attempts`: Scroll pogingen om posts te laden (3)

---

## 🎮 **Interactieve Commando's**

### 🖥️ **Console Commando's**
Terwijl bot draait, typ:
- `status` - Toon huidige bot status en configuratie
- `stats` - Toon vandaag's comment statistieken per account
- `pause` - Pauzeer bot operatie (kan hervat worden)
- `resume` - Hervat gepauzeerde bot operatie
- `stop` - Stop bot gracefully (voltooit huidige sessie)
- `quit` - Forceer onmiddellijk afsluiten
- `help` - Toon beschikbare commando's

### 📱 **Telegram Commando's** (indien ingeschakeld)
Stuur naar je Telegram bot:
- `/status` - Toon huidige bot status en configuratie
- `/stats` - Toon vandaag's comment statistieken per account
- `/pause` - Pauzeer bot operatie (kan hervat worden)
- `/resume` - Hervat gepauzeerde bot operatie
- `/stop` - Stop bot gracefully (voltooit huidige sessie)
- `/help` - Toon beschikbare Telegram commando's

---

## 🧠 **Hoe Het Werkt**

1. **Account Rotatie**: Roteert door meerdere Instagram accounts
2. **Slim Inloggen**: Gebruikt opgeslagen cookies om inloggen over te slaan wanneer mogelijk
3. **Dagelijkse Limieten**: Respecteert per-account dagelijkse comment limieten
4. **Hashtag Verwerking**: Verwerkt willekeurig geconfigureerde hashtags
5. **Post Ontdekking**: Scrollt en vindt posts voor elke hashtag
6. **Duplicaat Preventie**: Slaat posts over waar al op gecommentarieerd is
7. **Comment Plaatsing**: Plaatst willekeurige comments uit jouw lijst
8. **Statistiek Tracking**: Registreert alle activiteit in JSON formaat
9. **Proxy Rotatie**: Gebruikt snelle, geverifieerde proxies voor elke sessie
10. **Real-time Controle**: Reageer op console/Telegram commando's

---

## 📊 **Statistieken & Monitoring**

De bot houdt automatisch bij:
- Dagelijkse comment aantallen per account
- URLs waar op gecommentarieerd is (voorkomt duplicaten)
- Comment tekst gebruikt voor elke post
- Succes/faal percentages
- Alle data opgeslagen in `comment_stats.json`

Voorbeeld stats output:
```
📈 Vandaag's Statistieken (2025-07-24):
   account1: 15 comments
   account2: 23 comments
   account3: 8 comments
📊 Totaal: 46 comments vandaag
```

---

## 🚀 **Gebruiksvoorbeelden**

### **Basis Gebruik**
```bash
# Eerste keer setup
python main.py --setup

# Run de bot
python main.py
```

### **Geavanceerd Gebruik**
```bash
# Maak aangepaste config
python main.py --create-config
# Bewerk bot_config_sample.json en hernoem naar bot_config.json

# Run met bestaande config
python main.py
```

### **Telegram Setup**
1. Stuur bericht naar @BotFather op Telegram
2. Maak bot met `/newbot`
3. Krijg jouw bot token
4. Stuur bericht naar jouw bot, bezoek dan `https://api.telegram.org/bot<TOKEN>/getUpdates`
5. Vind jouw chat ID in de response
6. Voeg beide toe aan bot configuratie

---

## 📱 **Telegram Bot Setup Gids**

1. **Maak Bot**:
   - Stuur bericht naar @BotFather op Telegram
   - Stuur `/newbot`
   - Kies naam en gebruikersnaam
   - Bewaar het bot token

2. **Krijg Chat ID**:
   - Stuur bericht naar jouw nieuwe bot
   - Bezoek: `https://api.telegram.org/bot<JOUW_TOKEN>/getUpdates`
   - Vind jouw chat ID in de JSON response

3. **Configureer**:
   - Voeg token en chat ID toe tijdens setup
   - Bot zal automatisch remote control inschakelen

---

## 📜 **Disclaimer**

Deze tool interacteert met Instagram en kan hun [Terms of Service](https://help.instagram.com/581066165581870) schenden.  
**Gebruik op eigen risico.** Jouw accounts kunnen geblokkeerd of gemarkeerd worden bij overmatig of verkeerd gebruik.

- ✅ **WEL DOEN**: Gebruik voor vreedzaam bewustzijn en educatie
- ❌ **NIET DOEN**: Gebruik voor spam, intimidatie, of commerciële promotie
- 🎓 **Doel**: Dit project is voor **educatieve doeleinden** en humanitair bewustzijn
- 🔒 **Verantwoordelijkheid**: Ligt volledig bij **jou**

---

## 🛡️ **Veiligheidsfeatures**

- **Rate Limiting**: Automatische vertragingen tussen acties
- **Dagelijkse Limieten**: Voorkomt overmatig gebruik van accounts
- **Error Handling**: Graceful failure recovery
- **Sessie Management**: Juiste cookie handling
- **Duplicaat Preventie**: Nooit dubbel commentariëren
- **Graceful Shutdown**: Schone exit op stop commando's

---

## 🆘 **Probleemoplossing**

### Veelvoorkomende Problemen:
- **ChromeDriver Error**: Download juiste versie van [ChromeDriver](https://chromedriver.chromium.org/)
- **Login Mislukt**: Controleer account gegevens in `accounts.txt`
- **Geen Proxies**: Schakel proxy gebruik uit of voeg werkende proxies toe
- **Telegram Werkt Niet**: Verifieer token en chat ID

### Hulp Krijgen:
```bash
python main.py --help
```

---

## ❤️ **Laatste Woord**

> "Wanneer onrecht wet wordt, wordt verzet plicht."  
> Spreek je uit. Zelfs online. Zelfs met code.  
> Vooral wanneer ze proberen de stemmen van de onderdrukten het zwijgen op te leggen.

🇵🇸 **Vrij Palestina. Leve het verzet.**

---

**Gemaakt met 💚 voor digitaal activisme en Palestijns bewustzijn**