'''
Lo scopo principale di urls.py a livello di progetto è instradare le richieste degli utenti alle varie parti del tuo sito web. Può includere rotte per le pagine principali, l'interfaccia di amministrazione, 
le pagine di autenticazione e qualsiasi altra funzionalità del tuo sito. Organizzare correttamente le rotte in urls.py è fondamentale per garantire che gli utenti possano accedere alle diverse parti del tuo sito in modo coerente e intuitivo.

Per quanto riguarda il collegamento tra una view e un URL, Django associa una view a un URL utilizzando il file urls.py. 
Tuttavia, non è sempre pratico o possibile specificare l'URL direttamente nella definizione della view. Quindi, reverse_lazy (o reverse) viene utilizzato per ottenere l'URL corretto in modo dinamico in base al nome della view, rendendo il 
codice più flessibile e manutenibile.

'''


from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from django.conf.urls.static import static

urlpatterns = [
    # Redirect alla vista 'home' se l'utente è autenticato, altrimenti reindirizza a '/login/'.
    # È necessario importare le funzioni e classi usate qui.
    path('', login_required(RedirectView.as_view(url=reverse_lazy('home')), login_url='/login/'), name='root'), #In questo caso la home è un nome dato negli urls.py della app tracker interna.
    

'''
     - path('', ...): Questa riga definisce la route per la radice del tuo sito web. Quando un utente accede al dominio del tuo sito senza specificare alcun percorso aggiuntivo, questa route viene attivata.
     - login_required(...): Questa è una funzione decorator di Django che viene utilizzata per assicurarsi che solo gli utenti autenticati possano accedere alla view associata. Nel contesto di questa riga di codice, login_required è 
                            utilizzato per proteggere l'accesso alla RedirectView che reindirizza gli utenti autenticati alla home page del sito.
     - RedirectView.as_view(url=reverse_lazy('home')): RedirectView è una classe generica di Django utilizzata per reindirizzare gli utenti da una URL a un'altra. In questo caso, stiamo creando un'istanza di RedirectView e specificando che 
                            gli utenti devono essere reindirizzati alla URL della home page ('home') del nostro sito. Il metodo as_view() è necessario per convertire la classe in una view che può essere utilizzata nelle definizioni di URL.
     - reverse_lazy('home'): reverse_lazy è una funzione di utilità di Django che consente di ottenere l'URL inverso per una data view. Nel nostro caso, stiamo ottenendo l'URL inverso per la home page del nostro sito, che è stata definita con 
                            il nome 'home'. Utilizziamo reverse_lazy anziché reverse perché viene valutato solo quando necessario, in questo caso durante l'inizializzazione della URL.
     - login_url='/login/': Questo parametro specifica l'URL a cui gli utenti non autenticati devono essere reindirizzati se cercano di accedere alla view protetta da login_required. In questo caso, se un utente non autenticato cerca di accedere 
                            alla radice del sito, verrà reindirizzato alla pagina di login, che ha l'URL '/login/'.
     - name='root': Questo è il nome assegnato a questa route, che può essere utilizzato per fare riferimento ad essa all'interno del codice Python. Ad esempio, potresti utilizzare questo nome per generare URL all'interno dei tuoi template usando 
                            il tag {% url 'root' %}.

In sintesi, questa riga di codice definisce una route per la radice del tuo sito web che reindirizza gli utenti autenticati alla home page del sito e reindirizza gli utenti non autenticati alla pagina di login se cercano di accedere alla radice.

'''

    # Mappa tutte le richieste che iniziano con 'admin/' al modulo amministrativo di Django.
    # Questo è il percorso standard per accedere all'interfaccia di amministrazione di Django.
    path('admin/', admin.site.urls, name="admin"),
    
    # Definisce la route per la pagina di login utilizzando la vista built-in di Django.
    # 'LoginView.as_view()' crea una class-based view per il login.
    path('login/', LoginView.as_view(), name='login'),

     path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



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