from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Mappa tutte le richieste che iniziano con 'admin/' al modulo amministrativo di Django.
    path('accounts/', include('django.contrib.auth.urls')),  # Include le URL per le funzionalità di autenticazione fornite da Django.
    path('', include('tracker.urls')),  # Includi le URL definite nella app 'tracker', gestendo tutte le richieste alla root dell'applicazione.
]


'''

1. **`from django.contrib import admin`**:
   - Questo importa le funzionalità amministrative di Django, permettendoti di utilizzare `admin.site.urls`. 
   Questa è una configurazione predefinita che collega il pannello di amministrazione di Django con il tuo sito web, consentendo agli amministratori di gestire il contenuto del sito.

2. **`from django.urls import path, include`**:
   - `path()`: Questa funzione è utilizzata per definire un percorso URL. Ogni percorso può essere associato a una vista specifica, che gestirà le richieste a quel percorso.
   - `include()`: Questa funzione permette di includere altre configurazioni URL da altre app all'interno del progetto principale. Questo aiuta a mantenere il codice pulito e ben organizzato, permettendo a ciascuna app di gestire le proprie URL.

3. **`urlpatterns`**:
   - Questa lista contiene tutte le definizioni degli URL per il tuo progetto. Django usa questa lista per decidere cosa fare quando riceve una richiesta HTTP.

4. **Dettaglio dei Percorsi Definiti**:
   - `path('admin/', admin.site.urls)`: Collega l'URL `admin/` al modulo amministrativo di Django. Per esempio, se visiti `http://yourwebsite.com/admin/`, verrai indirizzato al pannello di amministrazione di Django.
   - `path('accounts/', include('django.contrib.auth.urls'))`: Include un insieme predefinito di URL per la gestione dell'autenticazione, come il login, il logout, e la gestione delle password. Django fornisce queste URL per facilitare la gestione degli utenti senza dover riscrivere il codice comune per queste operazioni.
   - `path('', include('tracker.urls'))`: Questo percorso dice a Django di includere le URL definite nell'app `tracker` per qualsiasi richiesta alla radice del sito. Ciò significa che tutte le configurazioni URL in `tracker/urls.py` saranno applicate partendo dalla root del sito. Questo è particolarmente utile per mantenere separate le configurazioni URL di diverse app.

Questi componenti lavorano insieme per dirigere il traffico nel tuo sito, garantendo che le richieste degli utenti siano gestite efficacemente e che ogni parte del sito sia facilmente accessibile e sicura.
'''