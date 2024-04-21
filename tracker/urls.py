from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Mappa la vista della home page
    path('add/', views.add_activity, name='add_activity'),  # Mappa la vista per aggiungere una nuova attività
    path('edit/<int:pk>/', views.edit_activity, name='edit_activity'),  # Mappa la vista per modificare un'attività
    path('delete/<int:pk>/', views.delete_activity, name='delete_activity'),  # Mappa la vista per eliminare un'attività
    path('complete/<int:pk>/', views.complete_activity, name='complete_activity'),  # Mappa la vista per completare un'attività
    path('delete_log/<int:pk>/', views.delete_activity_log, name='delete_activity_log'),  # Mappa la vista per eliminare un log di attività
    path('delete_30days_log/<int:pk>/', views.delete_old_logs, name='delete_activity_30days_log'),  # Mappa la vista per eliminare un log di attività
    
]




'''
### Spiegazione del Codice:

1. **`from django.urls import path`**:
   - `path()`: È una funzione utilizzata per definire i percorsi URL nella tua app Django. Per ogni URL che vuoi gestire, utilizzi `path()` per mapparlo a una vista specifica, 
   che sarà responsabile del trattamento delle richieste a quel particolare URL.

2. **`from . import views`**:
   - Questo comando importa il modulo `views` dalla stessa directory dell'app `tracker`. 
   Il modulo `views` contiene le funzioni che gestiscono la logica di risposta alle richieste HTTP. Utilizzando `from . import views`, assicuri che `path()` possa fare 
   riferimento alle viste definite in questo modulo.

3. **`urlpatterns`**:
   - `urlpatterns` è una lista di pattern di URL che Django utilizza per dirigere le richieste in entrata verso le corrette viste. Ogni elemento nella lista è una chiamata alla funzione `path()`, che definisce un particolare percorso URL e specifica quale vista deve rispondere a quel percorso.

4. **Dettaglio del Percorso Definito**:
   - `path('', views.home, name='home')`: Questa riga definisce un pattern di URL che associa la root della tua app (`''`) alla vista `home` definita nel modulo `views`. 
   In altre parole, quando un utente visita la root URL della tua app (ad esempio, `http://yourwebsite.com/` se la tua app è montata sulla root del sito), 
   Django invoca la funzione `home` nel modulo `views` per gestire la richiesta. 
   L'argomento `name='home'` fornisce un nome che può essere utilizzato per fare riferimento a questo percorso specifico altrove nel tuo progetto, 
   specialmente quando si utilizzano funzioni come `reverse` o tag di template per generare URL.

Questo file `urls.py` è essenziale per assicurare che le richieste degli utenti vengano correttamente indirizzate alle parti appropriate della tua app `tracker`. Definisce chiaramente quale vista deve rispondere a un determinato percorso, aiutando a mantenere organizzata la gestione del traffico web della tua app.

'''